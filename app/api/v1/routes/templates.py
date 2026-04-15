from fastapi import APIRouter, HTTPException
from app.core.templates.engine import template_engine
from app.core.enums import TemplateType

router = APIRouter(prefix="/templates", tags=["templates"])

_PREVIEWS = {
    TemplateType.ANCHOR_READING_PASSAGE: {
        "title": "The Young Inventor's Challenge",
        "passage_text": "Sarah stared at the pile of recycled materials in her garage...",
        "reading_level": "7.2",
        "word_count": 650,
        "key_vocabulary": [
            "innovation: creating new ideas or methods",
            "perseverance: continuing despite difficulties",
        ],
        "main_theme": "Problem-solving through creativity and determination",
        "discussion_questions": [
            "How did Sarah demonstrate perseverance?",
            "What role did creativity play in solving the problem?",
        ],
    },
    TemplateType.BUNDLE_OVERVIEW: {
        "title": "Bundle Overview",
        "standard_alignment_title": "Standard Alignment",
        "standard_alignment_content": "This bundle aligns with Common Core ELA standards...",
        "whats_included_title": "What's Included",
        "whats_included_content": "Reading passage, comprehension questions, vocabulary pack, short quiz, exit tickets, writing prompts.",
        "learning_objectives_title": "Learning Objectives",
        "learning_objectives_content": "Students will analyze theme, identify key vocabulary, and demonstrate comprehension.",
    },
    TemplateType.EXIT_TICKETS: {
        "title": "Exit Tickets",
        "objectives": "Check for understanding of today's reading standard.",
        "directions": "Answer each question in 2–3 sentences.",
        "tickets": [
            {"number": 1, "title": "Main Idea", "question": "What is the main idea of the passage?", "sample_answer": "The main idea is..."},
            {"number": 2, "title": "Key Detail", "question": "Identify one key detail that supports the main idea.", "sample_answer": "One key detail is..."},
        ],
        "answer_key_title": "Answer Key",
    },
    TemplateType.READING_COMPREHENSION_QUESTIONS: {
        "title": "Reading Comprehension Questions",
        "objectives": "Demonstrate understanding of the text through literal and inferential questions.",
        "directions": "Answer each question using evidence from the text.",
        "question_type_1_title": "Literal Questions",
        "question_type_2_title": "Inferential Questions",
        "questions": [
            {"number": 1, "question": "What happened at the beginning of the story?", "answer": "At the beginning..."},
            {"number": 6, "question": "What can you infer about the character's motivation?", "answer": "Based on the text..."},
        ],
        "answer_key_title": "Answer Key",
    },
    TemplateType.SHORT_QUIZ: {
        "title": "Short Quiz",
        "objectives": "Assess understanding of the reading standard.",
        "directions": "Answer all questions. Write in complete sentences where required.",
        "questions": [
            {"number": 1, "question": "What is the central theme of the passage?", "answer": "The central theme is..."},
            {"number": 2, "question": "How does the author develop the theme?", "answer": "The author develops the theme by..."},
        ],
        "answer_key_title": "Answer Key",
    },
    TemplateType.VOCABULARY_PACK: {
        "title": "Vocabulary Pack",
        "objectives": "Learn and apply key vocabulary from the reading standard.",
        "directions": "Study each word, its definition, and example sentence.",
        "vocabulary_words": [
            {"number": 1, "word": "analyze", "definition": "to examine in detail", "sentence": "We will analyze the author's word choice."},
            {"number": 2, "word": "infer", "definition": "to conclude from evidence", "sentence": "Readers can infer the character's feelings."},
        ],
        "quiz_header": "Vocabulary Quiz",
        "quiz_direction": "Match each word to its definition.",
        "quiz_questions": [
            {"number": 1, "question": "What does 'analyze' mean?", "answer": "To examine in detail"},
        ],
        "answer_key_title": "Answer Key",
    },
    TemplateType.WRITING_PROMPTS: {
        "title": "Writing Prompts",
        "objectives": "Practice structured writing aligned with the ELA standard.",
        "directions": "Choose one prompt and write a well-organized response of at least 3 paragraphs.",
        "prompts": [
            {"number": 1, "title": "Theme Analysis", "content": "Analyze the central theme of the passage. Use at least two pieces of evidence."},
            {"number": 2, "title": "Character Study", "content": "Describe how the main character changes throughout the story."},
            {"number": 3, "title": "Author's Purpose", "content": "Explain the author's purpose and how it influences the text."},
        ],
        "exemplar_title": "Writing Exemplar",
        "exemplar_subtitle": "Sample Response",
        "exemplar_content": "The central theme of this passage is perseverance. The author demonstrates this through...",
    },
}


@router.get("")
async def get_available_templates():
    """Get list of available template types"""
    return {
        "templates": [template.value for template in template_engine.get_available_templates()]
    }


@router.get("/{template_type}")
async def get_template_structure(template_type: TemplateType):
    """Get template structure and constraints"""
    try:
        structure = template_engine.get_template_structure(template_type)
        return {"data": structure}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{template_type}/preview")
async def get_template_preview(template_type: TemplateType):
    """Get template preview with example content"""
    try:
        preview = _PREVIEWS.get(template_type)
        if not preview:
            raise HTTPException(status_code=404, detail="Preview not available for this template")
        return {
            "template_type": template_type,
            "preview": preview,
            "structure": template_engine.get_template_structure(template_type),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
