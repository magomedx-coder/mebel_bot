from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Iterable, List, Optional

from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Category, Product, Lead, ProductType, ProductPhoto


# SQLite database file in the same directory as this module
DATABASE_URL = f"sqlite:///" + __file__.replace("\\", "/").rsplit("/", 1)[0] + "/app.db"

engine = create_engine(
	DATABASE_URL,
	echo=False,
	future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
	"""Create all tables if they do not exist."""
	Base.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
	"""Provide a transactional scope around a series of operations."""
	session: Session = SessionLocal()
	try:
		yield session
		session.commit()
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()


# -----------------------------
# CRUD for Category
# -----------------------------
def get_category_by_slug(session: Session, slug: str) -> Optional[Category]:
	stmt = select(Category).where(Category.slug == slug)
	return session.scalar(stmt)


def get_category_by_id(session: Session, category_id: int) -> Optional[Category]:
	stmt = select(Category).where(Category.id == category_id)
	return session.scalar(stmt)


def create_category(session: Session, *, slug: str, name: str, parent_id: Optional[int] = None, sort_order: int = 0) -> Category:
	category = Category(slug=slug, name=name, parent_id=parent_id, sort_order=sort_order)
	session.add(category)
	session.flush()
	return category


def list_categories(session: Session, parent_id: Optional[int] = None) -> List[Category]:
	stmt = select(Category)
	if parent_id is None:
		stmt = stmt.where(Category.parent_id.is_(None))
	else:
		stmt = stmt.where(Category.parent_id == parent_id)
	stmt = stmt.order_by(Category.sort_order.asc(), Category.name.asc())
	return list(session.scalars(stmt).all())


def get_category_tree(session: Session) -> List[Category]:
	"""Получить все категории с детьми"""
	stmt = select(Category).where(Category.parent_id.is_(None)).order_by(Category.sort_order.asc())
	return list(session.scalars(stmt).all())


# -----------------------------
# CRUD for ProductType
# -----------------------------
def create_product_type(session: Session, *, name: str, slug: str, description: Optional[str] = None) -> ProductType:
	product_type = ProductType(name=name, slug=slug, description=description)
	session.add(product_type)
	session.flush()
	return product_type


def get_product_type_by_slug(session: Session, slug: str) -> Optional[ProductType]:
	stmt = select(ProductType).where(ProductType.slug == slug)
	return session.scalar(stmt)


def list_product_types(session: Session) -> List[ProductType]:
	stmt = select(ProductType).order_by(ProductType.name.asc())
	return list(session.scalars(stmt).all())


# -----------------------------
# CRUD for Product
# -----------------------------
def create_product(
	session: Session,
	*,
	category: Category,
	country: str,
	title: str,
	description: str,
	price: Optional[float] = None,
	dimensions: Optional[str] = None,
	product_type: Optional[ProductType] = None,
	in_stock: bool = True,
	sort_order: int = 0,
) -> Product:
	product = Product(
		category=category,
		country=country,
		title=title,
		description=description,
		price=price,
		dimensions=dimensions,
		product_type=product_type,
		in_stock=in_stock,
		sort_order=sort_order,
	)
	session.add(product)
	session.flush()
	return product


def get_product(session: Session, product_id: int) -> Optional[Product]:
	stmt = select(Product).where(Product.id == product_id)
	return session.scalar(stmt)


def list_products(
	session: Session,
	*,
	category_id: Optional[int] = None,
	category_slug: Optional[str] = None,
	country: Optional[str] = None,
	product_type_id: Optional[int] = None,
	limit: Optional[int] = None,
) -> List[Product]:
	stmt = select(Product)
	if category_id:
		stmt = stmt.where(Product.category_id == category_id)
	elif category_slug:
		stmt = stmt.join(Product.category).where(Category.slug == category_slug)
	if country:
		stmt = stmt.where(Product.country == country)
	if product_type_id:
		stmt = stmt.where(Product.product_type_id == product_type_id)
	stmt = stmt.order_by(Product.sort_order.asc(), Product.title.asc())
	if limit:
		stmt = stmt.limit(limit)
	return list(session.scalars(stmt).all())


def add_product_photo(session: Session, *, product: Product, photo_url: str, sort_order: int = 0, is_main: bool = False) -> ProductPhoto:
	photo = ProductPhoto(
		product=product,
		photo_url=photo_url,
		sort_order=sort_order,
		is_main=is_main
	)
	session.add(photo)
	session.flush()
	return photo


def update_product(
	session: Session,
	product_id: int,
	*,
	data: dict,
) -> Optional[Product]:
	stmt = update(Product).where(Product.id == product_id).values(**data).execution_options(synchronize_session="fetch")
	session.execute(stmt)
	return get_product(session, product_id)


def delete_product(session: Session, product_id: int) -> None:
	stmt = delete(Product).where(Product.id == product_id)
	session.execute(stmt)


# -----------------------------
# Leads
# -----------------------------
def create_lead(
	session: Session, 
	*, 
	name: str, 
	phone: str, 
	product_id: Optional[int] = None,
	interest_type: str = "order",
	comment: Optional[str] = None
) -> Lead:
	lead = Lead(
		name=name, 
		phone=phone, 
		product_id=product_id,
		interest_type=interest_type,
		comment=comment
	)
	session.add(lead)
	session.flush()
	return lead


def list_leads(session: Session, status: Optional[str] = None, limit: Optional[int] = None) -> List[Lead]:
	stmt = select(Lead)
	if status:
		stmt = stmt.where(Lead.status == status)
	stmt = stmt.order_by(Lead.created.desc())
	if limit:
		stmt = stmt.limit(limit)
	return list(session.scalars(stmt).all())


def update_lead_status(session: Session, lead_id: int, status: str) -> Optional[Lead]:
	stmt = update(Lead).where(Lead.id == lead_id).values(status=status).execution_options(synchronize_session="fetch")
	session.execute(stmt)
	stmt_select = select(Lead).where(Lead.id == lead_id)
	return session.scalar(stmt_select)


__all__ = [
	"engine",
	"SessionLocal",
	"init_db",
	"get_session",
	"create_category",
	"list_categories",
	"get_category_tree",
	"get_category_by_slug",
	"get_category_by_id",
	"create_product_type",
	"list_product_types",
	"get_product_type_by_slug",
	"create_product",
	"add_product_photo",
	"list_products",
	"get_product",
	"update_product",
	"delete_product",
	"create_lead",
	"list_leads",
	"update_lead_status",
]