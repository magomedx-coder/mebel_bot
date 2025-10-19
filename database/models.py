from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    parent: Mapped[Optional["Category"]] = relationship("Category", remote_side=[id], back_populates="children")
    children: Mapped[List["Category"]] = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    products: Mapped[List["Product"]] = relationship(back_populates="category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, slug={self.slug!r}, name={self.name!r})"


class ProductType(Base):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"ProductType(id={self.id!r}, name={self.name!r})"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), index=True)
    product_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("product_types.id"), nullable=True)
    country: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    dimensions: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    category: Mapped[Category] = relationship(back_populates="products")
    product_type: Mapped[Optional[ProductType]] = relationship()
    photos: Mapped[List["ProductPhoto"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, title={self.title!r}, price={self.price!r})"


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    photo_url: Mapped[str] = mapped_column(String(512))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    product: Mapped[Product] = relationship(back_populates="photos")

    def __repr__(self) -> str:
        return f"ProductPhoto(id={self.id!r}, product_id={self.product_id!r})"


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(64))
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"), nullable=True)
    interest_type: Mapped[str] = mapped_column(String(32), default="order")  # order, consultation, question
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="new")  # new, in_progress, closed
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product: Mapped[Optional[Product]] = relationship()

    def __repr__(self) -> str:
        return f"Lead(id={self.id!r}, name={self.name!r}, phone={self.phone!r}, status={self.status!r})"