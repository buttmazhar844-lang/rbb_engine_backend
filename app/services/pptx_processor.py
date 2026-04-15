from pptx import Presentation
from pptx.util import Pt
from pptx.oxml.ns import qn
from lxml import etree
from pathlib import Path
from typing import Dict, Any
from app.utils.logger import logger
from app.utils.storage import storage_manager
import os

SKIP_TOKENS = {"{{STUDENT_NAME}}", "{{DATE}}"}


class PPTXProcessor:
    """Fill v3 PPTX templates by replacing {{TOKEN}} strings in TextBoxes"""

    def __init__(self):
        templates_dir = os.getenv('TEMPLATES_DIR', Path(__file__).parent.parent.parent / 'Templates')
        self.templates_dir = Path(templates_dir)

    def _template_path(self, filename: str) -> Path:
        return self.templates_dir / filename

    def _lines_that_fit(self, height_inches: float, font_pt: int) -> int:
        return int((height_inches * 72) / (font_pt * 1.3))

    def _chars_per_line(self, width_inches: float, font_pt: int) -> int:
        return int((width_inches * 72) / (font_pt * 0.52))

    def _truncate_to_box(self, text: str, width_in: float, height_in: float, font_pt: int) -> str:
        max_lines = self._lines_that_fit(height_in, font_pt)
        cpl = self._chars_per_line(width_in, font_pt)
        result = []
        total = 0
        for line in text.split('\n'):
            if total >= max_lines:
                break
            wrapped = max(1, (len(line) + cpl - 1) // cpl)
            if total + wrapped > max_lines:
                remaining_chars = (max_lines - total) * cpl
                result.append(line[:remaining_chars])
                total = max_lines
            else:
                result.append(line)
                total += wrapped
        return '\n'.join(result)

    def _merge_paragraph_runs(self, para):
        runs = para.runs
        if len(runs) <= 1:
            return
        merged = "".join(r.text for r in runs)
        runs[0].text = merged
        for run in runs[1:]:
            run._r.getparent().remove(run._r)

    def _set_paragraphs(self, tf, text: str, font_pt: int, template_run_xml):
        txBody = tf._txBody
        for p in txBody.findall(qn('a:p')):
            txBody.remove(p)
        for line in text.split('\n'):
            p_elem = etree.SubElement(txBody, qn('a:p'))
            if line:
                r_elem = etree.SubElement(p_elem, qn('a:r'))
                if template_run_xml is not None:
                    orig_rPr = template_run_xml.find(qn('a:rPr'))
                    if orig_rPr is not None:
                        new_rPr = etree.fromstring(etree.tostring(orig_rPr))
                        new_rPr.set('sz', str(font_pt * 100))
                        r_elem.insert(0, new_rPr)
                    else:
                        rPr = etree.SubElement(r_elem, qn('a:rPr'))
                        rPr.set('lang', 'en-US')
                        rPr.set('sz', str(font_pt * 100))
                else:
                    rPr = etree.SubElement(r_elem, qn('a:rPr'))
                    rPr.set('lang', 'en-US')
                    rPr.set('sz', str(font_pt * 100))
                t_elem = etree.SubElement(r_elem, qn('a:t'))
                t_elem.text = line

    def _fill_shape(self, shape, token: str, value: str, font_pt: int) -> bool:
        if not hasattr(shape, 'text_frame'):
            return False
        tf = shape.text_frame
        tf.word_wrap = True
        for para in tf.paragraphs:
            self._merge_paragraph_runs(para)
        if token not in tf.text:
            return False
        template_run_xml = None
        for para in tf.paragraphs:
            for run in para.runs:
                if token in run.text:
                    template_run_xml = run._r
                    break
            if template_run_xml is not None:
                break
        w_in = shape.width  / 914400
        h_in = shape.height / 914400
        truncated = self._truncate_to_box(value, w_in, h_in, font_pt)
        self._set_paragraphs(tf, truncated, font_pt, template_run_xml)
        return True

    def _fill_slides(self, prs: Presentation, token_map: Dict[str, tuple]):
        """Fill all slides in a presentation using the token→(value, font_pt) map."""
        for slide in prs.slides:
            for shape in slide.shapes:
                if not hasattr(shape, 'text_frame'):
                    continue
                raw = shape.text_frame.text
                if any(skip in raw for skip in SKIP_TOKENS):
                    continue
                for token, (value, fpt) in token_map.items():
                    if token in raw:
                        self._fill_shape(shape, token, value, fpt)
                        break

    def _save(self, prs: Presentation, product_id: int, filename: str) -> Path:
        product_path = storage_manager.get_product_path(product_id)
        output_path = product_path / filename
        prs.save(str(output_path))
        logger.info(f"Saved -> {output_path}")
        return output_path

    # ------------------------------------------------------------------ #
    #  ANCHOR READING PASSAGE                                              #
    # ------------------------------------------------------------------ #
    def fill_anchor_reading_passage(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - ANCHOR_READING_PASSAGE product {product_id}")
        tpath = self._template_path("ANCHOR READING PASSAGE MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        title    = content_data.get('title', 'Reading Passage')
        passage  = content_data.get('passage_text', '')
        theme    = content_data.get('main_theme', '')
        dqs      = content_data.get('discussion_questions', [])
        vocab    = content_data.get('key_vocabulary', [])
        grade    = product_metadata.get('grade_level', 'N/A')
        standard = product_metadata.get('ela_standard_code', 'N/A')

        objectives = (
            "\u2022 Analyze the central theme and message\n"
            "\u2022 Understand key vocabulary in context\n"
            "\u2022 Engage in critical thinking through discussion"
        )
        directions = (
            "Read the passage carefully. Pay attention to the main theme "
            "and key vocabulary. Be prepared to discuss the questions that follow."
        )
        dq_text    = "\n\n".join([f"\u2022 {q}" for q in dqs])   if dqs   else ""
        vocab_text = "\n\n".join([f"\u2022 {v}" for v in vocab]) if vocab else ""
        parts = []
        if dq_text:
            parts.append("Discussion Questions:\n\n" + dq_text)
        if vocab_text:
            parts.append("Key Vocabulary:\n\n" + vocab_text)
        combined = "\n\n\n".join(parts)

        token_map = {
            "{{ANCHOR_READING_PASSAGE_HEADER}}":        (title,                   14),
            "{{ANCHOR_READING_PASSAGE_GRADE_INFO}}":    (f"Grade {grade}",        12),
            "{{ANCHOR_READING_PASSAGE_STANDARD_INFO}}": (f"Standard: {standard}", 12),
            "{{ANCHOR_READING_PASSAGE_OBJECTIVES}}":    (objectives,              10),
            "{{ANCHOR_READING_PASSAGE_DIRECTIONS}}":    (directions,              10),
            "{{ANCHOR_READING_PASSAGE_STORY_TITLE}}":   (title,                   13),
            "{{ANCHOR_READING_PASSAGE_SUBTITLE}}":      (theme,                    9),
            "{{ANCHOR_READING_PASSAGE_CONTENT}}":       (passage if len(prs.slides) < 3 else combined, 9),
        }

        # Slide 1 — header + passage preview
        s1 = prs.slides[0]
        for shape in s1.shapes:
            if not hasattr(shape, 'text_frame'):
                continue
            raw = shape.text_frame.text
            if any(skip in raw for skip in SKIP_TOKENS):
                continue
            for token, (value, fpt) in token_map.items():
                if token in raw:
                    self._fill_shape(shape, token, value, fpt)
                    break

        # Slide 2 — full passage
        if len(prs.slides) > 1:
            for shape in prs.slides[1].shapes:
                if hasattr(shape, 'text_frame') and "{{ANCHOR_READING_PASSAGE_CONTENT}}" in shape.text_frame.text:
                    self._fill_shape(shape, "{{ANCHOR_READING_PASSAGE_CONTENT}}", passage, 10)

        # Slide 3 — questions + vocab
        if len(prs.slides) > 2:
            for shape in prs.slides[2].shapes:
                if hasattr(shape, 'text_frame') and "{{ANCHOR_READING_PASSAGE_CONTENT}}" in shape.text_frame.text:
                    self._fill_shape(shape, "{{ANCHOR_READING_PASSAGE_CONTENT}}", combined, 10)

        return self._save(prs, product_id, "anchor_reading_passage.pptx")

    # ------------------------------------------------------------------ #
    #  BUNDLE OVERVIEW                                                     #
    # ------------------------------------------------------------------ #
    def fill_bundle_overview(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - BUNDLE_OVERVIEW product {product_id}")
        tpath = self._template_path("BUNDLE OVERVIEW MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        grade    = product_metadata.get('grade_level', 'N/A')
        standard = product_metadata.get('ela_standard_code', 'N/A')

        token_map = {
            "{{BUNDLE_OVERVIEW_HEADER}}":           (content_data.get('title', 'Bundle Overview'),                          14),
            "{{BUNDLE_OVERVIEW_GRADE_INFO}}":        (f"Grade {grade}",                                                      12),
            "{{BUNDLE_OVERVIEW_STANDARD_INFO}}":     (f"Standard: {standard}",                                               12),
            "{{STANDARD_ALIGNMENT_TITLE}}":          (content_data.get('standard_alignment_title', 'Standard Alignment'),    12),
            "{{STANDARD_ALIGNMENT_CONTENT}}":        (content_data.get('standard_alignment_content', ''),                    10),
            "{{STANDARD_BREAKDOWN_TITLE}}":          (content_data.get('standard_breakdown_title', 'Standard Breakdown'),    12),
            "{{STANDARD_BREAKDOWN_CONTENT}}":        (content_data.get('standard_breakdown_content', ''),                    10),
            "{{WHATS_INCLUDED_TITLE}}":              (content_data.get('whats_included_title', "What's Included"),           12),
            "{{WHATS_INCLUDED_CONTENT}}":            (content_data.get('whats_included_content', ''),                        10),
            "{{LEARNING_OBJECTIVES_TITLE}}":         (content_data.get('learning_objectives_title', 'Learning Objectives'),  12),
            "{{LEARNING_OBJECTIVES_CONTENT}}":       (content_data.get('learning_objectives_content', ''),                   10),
            "{{SUGGESTED_PACING_TITLE}}":            (content_data.get('suggested_pacing_title', 'Suggested Pacing'),        12),
            "{{SUGGESTED_PACING_CONTENT}}":          (content_data.get('suggested_pacing_content', ''),                      10),
            "{{MATERIALS_NEEDED_TITLE}}":            (content_data.get('materials_needed_title', 'Materials Needed'),        12),
            "{{MATERIALS_NEEDED_CONTENT}}":          (content_data.get('materials_needed_content', ''),                      10),
            "{{DIFFERENTIATION_TIPS_TITLE}}":        (content_data.get('differentiation_tips_title', 'Differentiation Tips'),12),
            "{{DIFFERENTIATION_TIPS_CONTENT}}":      (content_data.get('differentiation_tips_content', ''),                  10),
            "{{ASSESSMENT_OVERVIEW_TITLE}}":         (content_data.get('assessment_overview_title', 'Assessment Overview'),  12),
            "{{{{ASSESSMENT_OVERVIEW_CONTENT}}":     (content_data.get('assessment_overview_content', ''),                   10),
        }
        self._fill_slides(prs, token_map)
        return self._save(prs, product_id, "bundle_overview.pptx")

    # ------------------------------------------------------------------ #
    #  EXIT TICKETS                                                        #
    # ------------------------------------------------------------------ #
    def fill_exit_tickets(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - EXIT_TICKETS product {product_id}")
        tpath = self._template_path("EXIT TICKETS MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        grade    = product_metadata.get('grade_level', 'N/A')
        standard = product_metadata.get('ela_standard_code', 'N/A')
        tickets  = content_data.get('tickets', [])

        token_map = {
            "{{EXIT_TICKETS_HEADER}}":       (content_data.get('title', 'Exit Tickets'),    14),
            "{{EXIT_TICKETS_GRADE_INFO}}":   (f"Grade {grade}",                             12),
            "{{EXIT_TICKETS_STANDARD_INFO}}": (f"Standard: {standard}",                    12),
            "{{EXIT_TICKETS_OBJECTIVES}}":   (content_data.get('objectives', ''),           10),
            "{{EXIT_TICKETS_DIRECTIONS}}":   (content_data.get('directions', ''),           10),
            "{{EXIT_TICKETS_ANSWER_KEY_TITLE}}": (content_data.get('answer_key_title', 'Answer Key'), 12),
        }
        for i, ticket in enumerate(tickets[:5], start=1):
            token_map[f"{{{{EXIT_TICKET_TITLE_{i}}}}}"]            = (ticket.get('title', ''),         11)
            token_map[f"{{{{EXIT_TICKET_QUESTION_CONTENT_{i}}}}}"] = (ticket.get('question', ''),      10)
            token_map[f"{{{{EXIT_TICKET_LINES_FOR_ANSWER_{i}}}}}"] = ('',                              10)
            token_map[f"{{{{EXIT_TICKETS_SAMPLE_ANSWER_TITLE_{i}}}}}"]   = (ticket.get('title', ''),         11)
            token_map[f"{{{{EXIT_TICKETS_SAMPLE_ANSWER_CONTENT_{i}}}}}"] = (ticket.get('sample_answer', ''), 10)

        self._fill_slides(prs, token_map)
        return self._save(prs, product_id, "exit_tickets.pptx")

    # ------------------------------------------------------------------ #
    #  READING COMPREHENSION QUESTIONS                                     #
    # ------------------------------------------------------------------ #
    def fill_reading_comprehension_questions(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - READING_COMPREHENSION_QUESTIONS product {product_id}")
        tpath = self._template_path("READING COMP QUESTIONS MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        grade     = product_metadata.get('grade_level', 'N/A')
        standard  = product_metadata.get('ela_standard_code', 'N/A')
        questions = content_data.get('questions', [])

        token_map = {
            "{{READING_COMPREHENSION_QUESTIONS_HEADER}}":                  (content_data.get('title', 'Reading Comprehension Questions'), 14),
            "{{READING_COMPREHENSION_QUESTIONS_GRADE_INFO}}":              (f"Grade {grade}",                                             12),
            "{{READING_COMPREHENSION_QUESTIONS_STANDARD_INFO}}":           (f"Standard: {standard}",                                      12),
            "{{READING_COMPREHENSION_QUESTIONS_OBJECTIVES}}":              (content_data.get('objectives', ''),                           10),
            "{{READING_COMPREHENSION_QUESTIONS_DIRECTIONS}}":              (content_data.get('directions', ''),                           10),
            "{{READING_COMPREHENSION_QUESTIONS_TYPE_OF_QUESTION_TITLE_1}}": (content_data.get('question_type_1_title', 'Literal Questions'),     12),
            "{{READING_COMPREHENSION_QUESTIONS_TYPE_OF_QUESTION_TITLE_2}}": (content_data.get('question_type_2_title', 'Inferential Questions'), 12),
            "{{READING_COMPREHENSION_QUESTIONS_ANSWER_KEY_TITLE}}":        (content_data.get('answer_key_title', 'Answer Key'),           12),
        }
        for i, q in enumerate(questions[:10], start=1):
            token_map[f"{{{{READING_COMPREHENSION_QUESTION_CONTENT_{i}}}}}"]        = (q.get('question', ''), 10)
            token_map[f"{{{{READING_COMPREHENSION_QUESTION_ANSWER_CONTENT_{i}}}}}"] = (q.get('answer', ''),   10)

        self._fill_slides(prs, token_map)
        return self._save(prs, product_id, "reading_comprehension_questions.pptx")

    # ------------------------------------------------------------------ #
    #  SHORT QUIZ                                                          #
    # ------------------------------------------------------------------ #
    def fill_short_quiz(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - SHORT_QUIZ product {product_id}")
        tpath = self._template_path("SHORT QUIZ MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        grade     = product_metadata.get('grade_level', 'N/A')
        standard  = product_metadata.get('ela_standard_code', 'N/A')
        questions = content_data.get('questions', [])

        token_map = {
            "{{SHORT_QUIZ_HEADER}}":          (content_data.get('title', 'Short Quiz'),          14),
            "{{SHORT_QUIZ_GRADE_INFO}}":       (f"Grade {grade}",                                12),
            "{{SHORT_QUIZ_STANDARD_INFO}}":    (f"Standard: {standard}",                         12),
            "{{SHORT_QUIZ_OBJECTIVES}}":       (content_data.get('objectives', ''),              10),
            "{{SHORT_QUIZ_DIRECTIONS}}":       (content_data.get('directions', ''),              10),
            "{{SHORT_QUIZ_ANSWER_KEY_TITLE}}": (content_data.get('answer_key_title', 'Answer Key'), 12),
        }
        for i, q in enumerate(questions[:7], start=1):
            token_map[f"{{{{SHORT_QUIZ_QUESTION_CONTENT_{i}}}}}"] = (q.get('question', ''), 10)
            token_map[f"{{{{SHORT_QUIZ_ANSWER_CONTENT_{i}}}}}"]   = (q.get('answer', ''),   10)

        self._fill_slides(prs, token_map)
        return self._save(prs, product_id, "short_quiz.pptx")

    # ------------------------------------------------------------------ #
    #  VOCABULARY PACK                                                     #
    # ------------------------------------------------------------------ #
    def fill_vocabulary_pack(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - VOCABULARY_PACK product {product_id}")
        tpath = self._template_path("VOCABULARY PACK MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        grade    = product_metadata.get('grade_level', 'N/A')
        standard = product_metadata.get('ela_standard_code', 'N/A')
        words    = content_data.get('vocabulary_words', [])
        quiz_qs  = content_data.get('quiz_questions', [])

        token_map = {
            "{{VOCABULARY_PACK_HEADER}}":        (content_data.get('title', 'Vocabulary Pack'),          14),
            "{{VOCABULARY_PACK_GRADE_INFO}}":     (f"Grade {grade}",                                     12),
            "{{VOCABULARY_PACK_STANDARD_INFO}}":  (f"Standard: {standard}",                              12),
            "{{VOCABULARY_PACK_OBJECTIVES}}":     (content_data.get('objectives', ''),                   10),
            "{{VOCABULARY_PACK_DIRECTIONS}}":     (content_data.get('directions', ''),                   10),
            "{{VOCABULARY_PACK_TITLE}}":          (content_data.get('title', 'Vocabulary Pack'),         13),
            "{{VOCABULARY_QUIZ_HEADER}}":         (content_data.get('quiz_header', 'Vocabulary Quiz'),   13),
            "{{VOCABULARY_QUIZ_DIRECTION}}":      (content_data.get('quiz_direction', ''),               10),
            "{{VOCABULARY_QUIZ_ANSWER_KEY_TITLE}}": (content_data.get('answer_key_title', 'Answer Key'), 12),
        }
        for i, w in enumerate(words[:10], start=1):
            token_map[f"{{{{VOCABULARY_PACK_WORD_{i}}}}}"]               = (w.get('word', ''),       12)
            token_map[f"{{{{VOCABULARY_PACK_DEFINITION_CONTENT_{i}}}}}"] = (w.get('definition', ''), 10)
            token_map[f"{{{{VOCABULARY_PACK_SENTENCE_CONTENT_{i}}}}}"]   = (w.get('sentence', ''),   10)
        for i, q in enumerate(quiz_qs[:6], start=1):
            token_map[f"{{{{VOCABULARY_QUIZ_QUESTION_CONTENT_{i}}}}}"] = (q.get('question', ''), 10)
            token_map[f"{{{{VOCABULARY_QUIZ_ANSWER_CONTENT_{i}}}}}"]   = (q.get('answer', ''),   10)

        self._fill_slides(prs, token_map)
        return self._save(prs, product_id, "vocabulary_pack.pptx")

    # ------------------------------------------------------------------ #
    #  WRITING PROMPTS                                                     #
    # ------------------------------------------------------------------ #
    def fill_writing_prompts(self, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        logger.info(f"PPTX generation start - WRITING_PROMPTS product {product_id}")
        tpath = self._template_path("WRITING PROMPTS MS TEMPLATES v3.pptx")
        if not tpath.exists():
            raise FileNotFoundError(f"Template not found: {tpath}")
        prs = Presentation(str(tpath))

        grade    = product_metadata.get('grade_level', 'N/A')
        standard = product_metadata.get('ela_standard_code', 'N/A')
        prompts  = content_data.get('prompts', [])

        token_map = {
            "{{WRITING_PROMPT_PACK_HEADER}}":      (content_data.get('title', 'Writing Prompts'),          14),
            "{{WRITING_PROMPT_PACK_GRADE_INFO}}":  (f"Grade {grade}",                                      12),
            "{{WRITING_PROMPT_PACK_STANDARD_INFO}}": (f"Standard: {standard}",                             12),
            "{{WRITING_PROMPT_PACK_OBJECTIVES}}":  (content_data.get('objectives', ''),                    10),
            "{{WRITING_PROMPT_PACK_DIRECTIONS}}":  (content_data.get('directions', ''),                    10),
            "{{WRITING_PROMPT_PACK_TITLE}}":       (content_data.get('title', 'Writing Prompts'),          13),
            "{{WRITING_EXEMPLAR_TITLE}}":          (content_data.get('exemplar_title', 'Writing Exemplar'),12),
            "{{WRITING_EXEMPLAR_SUBTITLE}}":       (content_data.get('exemplar_subtitle', 'Sample Response'), 11),
            "{{WRITING_EXEMPLAR_CONTENT}}":        (content_data.get('exemplar_content', ''),               9),
        }
        for i, p in enumerate(prompts[:3], start=1):
            token_map[f"{{{{WRITING_PROMPT_TITLE_{i}}}}}"]   = (p.get('title', ''),   12)
            token_map[f"{{{{WRITING_PROMPT_CONTENT_{i}}}}}"] = (p.get('content', ''), 10)

        self._fill_slides(prs, token_map)
        return self._save(prs, product_id, "writing_prompts.pptx")

    # ------------------------------------------------------------------ #
    #  DISPATCHER                                                          #
    # ------------------------------------------------------------------ #
    def process_template(self, template_type: str, content_data: Dict[str, Any], product_metadata: Dict[str, Any], product_id: int) -> Path:
        dispatch = {
            'ANCHOR_READING_PASSAGE':          self.fill_anchor_reading_passage,
            'BUNDLE_OVERVIEW':                 self.fill_bundle_overview,
            'EXIT_TICKETS':                    self.fill_exit_tickets,
            'READING_COMPREHENSION_QUESTIONS': self.fill_reading_comprehension_questions,
            'SHORT_QUIZ':                      self.fill_short_quiz,
            'VOCABULARY_PACK':                 self.fill_vocabulary_pack,
            'WRITING_PROMPTS':                 self.fill_writing_prompts,
        }
        handler = dispatch.get(template_type.upper())
        if not handler:
            raise NotImplementedError(f"PPTX processing not implemented for: {template_type}")
        return handler(content_data, product_metadata, product_id)


# Global instance
pptx_processor = PPTXProcessor()
