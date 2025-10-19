from __future__ import annotations

from .db import (
	init_db, get_session, 
	create_category, create_product, create_product_type, create_lead,
	get_category_by_slug, get_product_type_by_slug
)


def seed() -> None:
	init_db()
	with get_session() as session:
		# Create main categories
		bedroom = create_category(session, slug="bedroom", name="🛏️ Спальная мебель", sort_order=1)
		kitchen = create_category(session, slug="kitchen", name="🍳 Кухонная мебель", sort_order=2)
		sofa = create_category(session, slug="sofa", name="🛋️ Мягкая мебель", sort_order=3)
		tables = create_category(session, slug="tables", name="📚 Столы и стулья", sort_order=4)
		cabinets = create_category(session, slug="cabinets", name="📺 Тумбы и комоды", sort_order=5)
		mattresses = create_category(session, slug="mattresses", name="🛏️ Матрасы", sort_order=6)
		wardrobes = create_category(session, slug="wardrobes", name="🚪 Шкафы", sort_order=7)

		# Create subcategories for bedroom
		bedroom_ru = create_category(session, slug="bedroom_ru", name="🇷🇺 Российская", parent_id=bedroom.id, sort_order=1)
		bedroom_tr = create_category(session, slug="bedroom_tr", name="🇹🇷 Турецкая", parent_id=bedroom.id, sort_order=2)
		
		# Create subcategories for kitchen
		kitchen_straight = create_category(session, slug="kitchen_straight", name="📐 Прямая", parent_id=kitchen.id, sort_order=1)
		kitchen_corner = create_category(session, slug="kitchen_corner", name="🔽 Угловая", parent_id=kitchen.id, sort_order=2)
		
		# Create subcategories for sofa
		sofa_ru = create_category(session, slug="sofa_ru", name="🇷🇺 Российская", parent_id=sofa.id, sort_order=1)
		sofa_tr = create_category(session, slug="sofa_tr", name="🇹🇷 Турецкая", parent_id=sofa.id, sort_order=2)
		sofa_ru_straight = create_category(session, slug="sofa_ru_straight", name="📐 Прямая", parent_id=sofa_ru.id, sort_order=1)
		sofa_ru_corner = create_category(session, slug="sofa_ru_corner", name="🔽 Угловая", parent_id=sofa_ru.id, sort_order=2)

		# Create product types
		straight_type = create_product_type(session, name="Прямая", slug="straight", description="Прямая форма")
		corner_type = create_product_type(session, name="Угловая", slug="corner", description="Угловая форма")
		russian_type = create_product_type(session, name="Российская", slug="russian", description="Российское производство")
		turkish_type = create_product_type(session, name="Турецкая", slug="turkish", description="Турецкое производство")

		# Create sample products
		create_product(
			session,
			category=kitchen_straight,
			country="RU",
			title="Кухонный гарнитур Nova",
			description="Модульный кухонный гарнитур, фасады МДФ. Прямая форма, современный дизайн.",
			price=74990.00,
			dimensions="300x60x90 см",
			product_type=straight_type,
		)
		
		create_product(
			session,
			category=kitchen_corner,
			country="RU",
			title="Кухонный гарнитур Corner Pro",
			description="Угловая кухня с максимальным использованием пространства.",
			price=89990.00,
			dimensions="280x280x90 см",
			product_type=corner_type,
		)
		
		create_product(
			session,
			category=sofa_ru_straight,
			country="RU",
			title="Диван Comfort Plus",
			description="Прямой диван с ортопедическим матрасом, тканевая обивка.",
			price=45990.00,
			dimensions="200x90x80 см",
			product_type=straight_type,
		)
		
		create_product(
			session,
			category=sofa_ru_corner,
			country="RU",
			title="Угловой диван Family",
			description="Угловой диван для большой семьи, механизм раскладывания.",
			price=67990.00,
			dimensions="280x180x80 см",
			product_type=corner_type,
		)
		
		create_product(
			session,
			category=bedroom_ru,
			country="RU",
			title="Кровать SoftSleep",
			description="Двуспальная кровать с подъемным механизмом, ЛДСП.",
			price=42990.00,
			dimensions="200x160x40 см",
			product_type=russian_type,
		)
		
		create_product(
			session,
			category=wardrobes,
			country="RU",
			title="Шкаф-купе Classic",
			description="Практичный шкаф-купе с зеркалом, ЛДСП, 3 двери.",
			price=35990.00,
			dimensions="240x60x220 см",
			product_type=russian_type,
		)


if __name__ == "__main__":
	seed()
	print("✅ Seed completed - Database populated with categories and sample products")



