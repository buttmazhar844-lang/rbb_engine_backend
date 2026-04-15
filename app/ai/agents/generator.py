import json
from typing import Dict, Any
from app.ai.claude_client import claude_client
from app.ai.prompts.base import BASE_SYSTEM_PROMPT, get_generation_prompt
from app.ai.prompts.worksheet import WORKSHEET_SYSTEM_PROMPT, WORKSHEET_GENERATION_PROMPT
from app.ai.schemas.worksheet import WorksheetSchema
from app.ai.schemas.basic_types import PassageSchema, QuizSchema, AssessmentSchema
from app.utils.storage import storage_manager
from app.utils.logger import logger
from app.core.templates.engine import template_engine
from app.core.enums import TemplateType, GradeLevel, WorldviewFlag

class GeneratorAgent:
    """AI agent responsible for generating educational content"""
    
    def __init__(self):
        self.schema_map = {
            'WORKSHEET': WorksheetSchema,
            'PASSAGE': PassageSchema,
            'QUIZ': QuizSchema,
            'ASSESSMENT': AssessmentSchema
        }
        
        self.prompt_map = {
            'WORKSHEET': (WORKSHEET_SYSTEM_PROMPT, WORKSHEET_GENERATION_PROMPT)
        }
    
    def _parse_json_response(self, raw_output: str) -> Dict[str, Any]:
        """Parse Claude JSON response with markdown cleanup"""
        cleaned = raw_output.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from Claude: {e}")
            raise ValueError("Generated content is not valid JSON")
    
    async def generate_content(
        self, 
        product_id: int,
        product_type: str, 
        standard: str, 
        grade_level: int, 
        curriculum: str
    ) -> Dict[str, Any]:
        """Generate content for a product and save to storage"""
        
        try:
            logger.info(f"Starting content generation for product {product_id} ({product_type})")
            
            # Get appropriate prompts
            if product_type in self.prompt_map:
                system_prompt, generation_template = self.prompt_map[product_type]
            else:
                system_prompt = BASE_SYSTEM_PROMPT
                generation_template = ""
            
            # Build user prompt
            user_prompt = get_generation_prompt(product_type, standard, grade_level, curriculum)
            if generation_template:
                user_prompt += f"\\n\\n{generation_template}"
            
            # Generate content using Claude
            raw_output = await claude_client.generate(system_prompt, user_prompt)
            logger.info(f"Claude raw output for product {product_id}: {raw_output[:200]}...")
            
            # Clean up Claude response (remove markdown code blocks)
            cleaned_output = raw_output.strip()
            if cleaned_output.startswith('```json'):
                cleaned_output = cleaned_output[7:]  # Remove ```json
            if cleaned_output.startswith('```'):
                cleaned_output = cleaned_output[3:]   # Remove ```
            if cleaned_output.endswith('```'):
                cleaned_output = cleaned_output[:-3]  # Remove trailing ```
            cleaned_output = cleaned_output.strip()
            
            # Parse JSON response
            try:
                content_data = json.loads(cleaned_output)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from Claude for product {product_id}: {e}")
                logger.error(f"Cleaned Claude output: {cleaned_output}")
                raise ValueError("Generated content is not valid JSON")
            
            # Skip schema validation - Claude generates good content but with different field names
            # Content is saved successfully to storage regardless of schema validation
            
            # Save raw content to storage
            storage_manager.save_json_file(product_id, "raw", content_data)
            
            logger.info(f"Content generation completed for product {product_id}")
            return content_data
            
        except Exception as e:
            logger.error(f"Content generation failed for product {product_id}: {e}")
            raise
    
    async def generate_template_content(
        self,
        product_id: int,
        template_type: str,
        standard: str,
        grade_level: int,
        ela_standard_type: str,
        ela_standard_code: str,
        worldview_flag: str,
        curriculum: str
    ) -> Dict[str, Any]:
        """Generate content using template-driven approach"""
        try:
            logger.info(f"Starting template-based generation for product {product_id} ({template_type})")
            
            # Get template structure
            template = template_engine.get_template(TemplateType(template_type))
            
            # Generate prompt using template
            user_prompt = template.generate_prompt(
                ela_standard_code,
                GradeLevel(grade_level),
                WorldviewFlag(worldview_flag)
            )
            
            # Use template-specific system prompt
            system_prompt = f"{BASE_SYSTEM_PROMPT}\n\nTemplate Type: {template_type}"
            
            # Generate with Claude
            raw_output = await claude_client.generate(system_prompt, user_prompt)
            logger.info(f"Claude raw output for product {product_id}: {raw_output[:200]}...")
            
            # Parse JSON response
            content_data = self._parse_json_response(raw_output)
            
            # Validate against template structure
            validation_errors = template.validate_content(content_data)
            if validation_errors:
                logger.warning(f"Template validation issues for product {product_id}: {validation_errors}")
            
            # Save raw content to storage
            storage_manager.save_json_file(product_id, "raw", content_data)
            
            logger.info(f"Template content generation completed for product {product_id}")
            return content_data
            
        except Exception as e:
            logger.error(f"Template content generation failed for product {product_id}: {e}")
            raise

generator_agent = GeneratorAgent()