from __future__ import annotations

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import get_session, list_products, get_category_by_slug


router = Router()


def _format_price(value: float) -> str:
	return f"{value:,.2f}".replace(",", " ")


def _product_card_text(title: str, description: str, price: float, in_stock: bool) -> str:
	stock = "В наличии" if in_stock else "Нет в наличии"
	return (
		f"<b>{title}</b>\n"
		f"{description}\n\n"
		f"Цена: <b>{_format_price(price)} ₽</b>\n"
		f"Статус: {stock}"
	)


# Эти функции теперь обрабатываются через callback_query в categories.py


@router.callback_query(F.data.startswith("details:"))
async def product_details(call: CallbackQuery) -> None:
	product_id = int(call.data.split(":", 1)[1])
	with get_session() as session:
		from database.db import get_product
		p = get_product(session, product_id)
		if not p:
			await call.answer("Товар не найден", show_alert=True)
			return
		text = _product_card_text(p.title, p.description, float(p.price), p.in_stock)
		await call.message.edit_text(text)
		await call.answer()
