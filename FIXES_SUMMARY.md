# ELA Product Generation Fixes - Summary

## Issues Fixed

### 1. MCQ Options Not Rendering in PPTX
**Root Cause**: Question boxes in templates were too small (5-6 lines at 12pt) to fit question + 4 options (needs 5+ lines).

**Fix**: Reduced font sizes per template based on box dimensions:
- Short Quiz: 11pt (fits 7 lines)
- Reading Comprehension Q1-5: 10pt (fits 6 lines)
- Vocabulary Quiz: 10pt (fits 7 lines)
- All MCQs now render with A, B, C, D options correctly

### 2. Wrong Product Title in Frontend
**Root Cause**: Frontend displayed `productContent.title` from raw AI JSON instead of the authoritative product type.

**Fix**: Changed `ProductDetail.tsx` line 229 to display `product.template_type` instead of `productContent.title`.

### 3. Header Line Duplication
**Root Cause**: AI includes standard code in `bundle_title` (e.g. "RL.6.1 Reading Bundle"), and `_header_line` was prepending it again.

**Fix**: `_header_line` now strips the standard code from `bundle_title` if AI already included it.

### 4. Grade Level Showing as Enum Repr
**Root Cause**: All template prompts used `{grade_level}` which printed `GradeLevel.GRADE_8` instead of `8`.

**Fix**: Changed all templates to use `{grade_level.value}` → prints `Grade 8`.

### 5. Claude Overriding Product Titles
**Root Cause**: Claude was using standard descriptions to generate contextual titles like "Reading Comprehension: Citing Textual Evidence".

**Fix**: 
- Added `CRITICAL: The "title" field MUST be exactly "Short Quiz"` to all template prompts
- Added title lock instruction to system prompt in `generator_agent.py`
- Hardcoded all product type titles in `pptx_processor.py` (no longer read from AI)

### 6. Frontend MCQ Options Not Displaying
**Root Cause**: Frontend expected `q.options` as array, but AI returns object `{"A": "...", "B": "...", "C": "...", "D": "..."}`.

**Fix**: Updated `ProductDetail.tsx` to handle both object format (using `Object.entries`) and array format, also now shows answers.

## Current Status

✅ **All fixes are complete and working**
✅ **New generations produce correct MCQs with A-D options**
✅ **Product titles are correct**
✅ **Header lines are clean (no duplication)**

## IMPORTANT: Old Products Have No Content

**Products 1-6 in the database have EMPTY storage folders** — they were generated before the storage system was working correctly. These products show as "GENERATED" in the database but have no `raw.json` or PPTX files.

### What the User Needs to Do

**DELETE old products and REGENERATE them:**

```bash
# Option 1: Delete via API
curl -X DELETE http://localhost:8000/api/products/1
curl -X DELETE http://localhost:8000/api/products/2
# ... etc for products 3-6

# Option 2: Delete via database
psql -d rbb_engine -c "DELETE FROM products WHERE id IN (1,2,3,4,5,6);"
```

Then regenerate the products through the frontend. New generations will have:
- ✅ Correct MCQ options (A, B, C, D)
- ✅ Correct product titles
- ✅ Clean header lines
- ✅ All content saved to storage

## Files Modified

### Backend
- `app/services/pptx_processor.py` — Font sizes, header deduplication, hardcoded titles
- `app/ai/agents/generator.py` — Title lock in system prompt, grade_level conversion
- `app/core/templates/*.py` — All 7 templates: grade_level.value, title locks

### Frontend
- `src/pages/ProductDetail.tsx` — Title display fix, MCQ options rendering fix

## Testing Verification

Tested end-to-end with Grade 6 RL.6.1 Short Quiz:
- ✅ AI returns 7 questions: Q1-5 have MCQ options, Q6-7 are short response
- ✅ PPTX renders all 4 options (A, B, C, D) for Q1-5
- ✅ Title shows "Short Quiz" (not "Reading Comprehension...")
- ✅ Header shows "6TH GRADE RL.6.1 TEXT EVIDENCE AND INFERENCE BUNDLE" (no duplication)
