import httpx
import time
from typing import Optional
from app.core.config import settings
from app.utils.logger import logger

class ClaudeClient:
    """Claude Sonnet 4 API client with timeout, retry, and error handling"""
    
    def __init__(self):
        self.api_key = settings.claude_api_key
        self.model = settings.claude_model
        self.timeout = settings.claude_timeout
        self.max_retries = settings.claude_max_retries
        self.base_url = "https://api.anthropic.com/v1/messages"
    
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text using Claude with retries and error handling"""
        
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not configured")
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 4000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(self.base_url, json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        result = response.json()
                        content = result["content"][0]["text"]
                        logger.info(f"Claude generation successful (attempt {attempt + 1})")
                        return content
                    else:
                        logger.warning(f"Claude API error {response.status_code}: {response.text}")
                        if attempt == self.max_retries - 1:
                            raise Exception(f"Claude API failed: {response.status_code}")
                        
            except httpx.TimeoutException:
                logger.warning(f"Claude timeout on attempt {attempt + 1}")
                if attempt == self.max_retries - 1:
                    raise Exception("Claude API timeout after retries")
                    
            except Exception as e:
                logger.error(f"Claude error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise
            
            # Wait before retry
            if attempt < self.max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Claude generation failed after all retries")

claude_client = ClaudeClient()