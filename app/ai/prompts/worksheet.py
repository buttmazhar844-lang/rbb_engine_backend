"""Worksheet-specific prompts for content generation"""

WORKSHEET_SYSTEM_PROMPT = """You are creating educational worksheets that are practical, engaging, and curriculum-aligned.

WORKSHEET REQUIREMENTS:
- Include clear title and instructions
- Provide 8-12 varied questions/activities
- Include answer key with explanations
- Ensure progressive difficulty
- Add visual elements descriptions where helpful
- Include extension activities for advanced learners

OUTPUT: Valid JSON only, following the worksheet schema exactly."""

WORKSHEET_GENERATION_PROMPT = """Create a comprehensive worksheet with:

STRUCTURE REQUIRED:
- Title (engaging and descriptive)
- Learning objectives (2-3 clear goals)
- Instructions for students
- Questions/activities (8-12 items with variety)
- Answer key with explanations
- Extension activities (2-3 optional challenges)
- Estimated completion time

QUESTION TYPES TO INCLUDE:
- Multiple choice (2-3 questions)
- Short answer (3-4 questions)  
- Problem solving (2-3 questions)
- Creative/application tasks (1-2 questions)

Ensure questions build from basic recall to higher-order thinking skills."""