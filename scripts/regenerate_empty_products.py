"""
Regenerate all products that have empty storage (no raw.json).
Run with: python scripts/regenerate_empty_products.py
"""
import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import get_db
from app.models.product import Product
from app.core.enums import ProductStatus
from app.ai.agents.generator import generator_agent
from app.services.pptx_processor import pptx_processor
from app.utils.storage import storage_manager
from app.utils.logger import logger


async def regenerate_product(product):
    pid = product.id
    product_path = storage_manager.get_product_path(pid)
    raw_json = product_path / "raw.json"

    product_metadata = {
        'grade_level': product.grade_level.value,
        'ela_standard_code': product.ela_standard_code,
        'ela_standard_type': product.ela_standard_type.value,
        'worldview_flag': product.worldview_flag.value,
        'curriculum_board': product.curriculum_board.value,
    }

    if raw_json.exists():
        # Re-generate PPTX from existing raw.json with latest formatting
        import json
        content = json.loads(raw_json.read_text())
        try:
            pptx_processor.process_template(
                template_type=product.template_type.value,
                content_data=content,
                product_metadata=product_metadata,
                product_id=pid,
            )
            print(f"  [PPTX]  product_{pid} PPTX regenerated from existing raw.json")
        except Exception as e:
            print(f"  [WARN]  product_{pid} PPTX regen failed: {e}")
        return True

    print(f"  [REGEN] product_{pid} ({product.template_type.value}, grade {product.grade_level.value}, {product.ela_standard_code})")

    try:
        content = await generator_agent.generate_template_content(
            product_id=pid,
            template_type=product.template_type.value,
            standard=product.ela_standard_code,
            grade_level=product.grade_level.value,
            ela_standard_type=product.ela_standard_type.value,
            ela_standard_code=product.ela_standard_code,
            worldview_flag=product.worldview_flag.value,
            curriculum=product.curriculum_board.value,
        )

        pptx_processor.process_template(
            template_type=product.template_type.value,
            content_data=content,
            product_metadata=product_metadata,
            product_id=pid,
        )

        print(f"  [OK]    product_{pid} regenerated successfully")
        return True

    except Exception as e:
        print(f"  [FAIL]  product_{pid}: {e}")
        return False


async def main():
    db = next(get_db())
    try:
        products = (
            db.query(Product)
            .filter(Product.status == ProductStatus.GENERATED)
            .order_by(Product.id)
            .all()
        )

        print(f"Found {len(products)} GENERATED products to check\n")

        ok = fail = skip = 0
        for p in products:
            result = await regenerate_product(p)
            if result:
                product_path = storage_manager.get_product_path(p.id)
                if (product_path / "raw.json").exists():
                    ok += 1
                else:
                    skip += 1
            else:
                fail += 1

        print(f"\nDone: {ok} regenerated, {skip} skipped (already had content), {fail} failed")
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
