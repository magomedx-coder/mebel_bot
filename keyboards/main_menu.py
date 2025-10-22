from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from database.db import get_session, list_categories
from typing import Optional


def get_main_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Создает главное меню с категориями мебели"""
    builder = InlineKeyboardBuilder()
    
    # Основные категории мебели
    builder.button(text="Спальная мебель", callback_data="category:bedroom")
    builder.button(text="Кухонная мебель", callback_data="category:kitchen")
    builder.button(text="Мягкая мебель", callback_data="category:soft")
    builder.button(text="Столы и стулья", callback_data="category:tables")
    builder.button(text="Тумбы и комоды", callback_data="category:cabinets")
    builder.button(text="Кровати", callback_data="category:beds")
    builder.button(text="Матрасы", callback_data="category:mattress")
    builder.button(text="Шкафы", callback_data="category:wardrobes")
    
    # Информационные разделы
    builder.button(text="О компании / Контакты", callback_data="about_company")
    builder.button(text="Сотрудничество", callback_data="cooperation")
    
    # Кнопка админ-панели для администраторов
    if is_admin:
        builder.button(text="Настройка бота", callback_data="admin_panel")
    
    # Устанавливаем по 2 кнопки в ряд
    builder.adjust(2)
    
    return builder.as_markup()


def get_subcategory_menu(category_slug: str) -> Optional[InlineKeyboardMarkup]:
    """Создает клавиатуру с подкатегориями для определенных категорий мебели"""
    builder = InlineKeyboardBuilder()
    
    if category_slug in ["bedroom", "soft", "tables"]:
        builder.button(text="🇷🇺 Россия", callback_data=f"subcategory:{category_slug}:russia")
        builder.button(text="🇹🇷 Турция", callback_data=f"subcategory:{category_slug}:turkey")
    elif category_slug == "kitchen":
        builder.button(text="Прямая кухня", callback_data=f"subcategory:kitchen:straight")
        builder.button(text="Угловая кухня", callback_data=f"subcategory:kitchen:corner")
    else:
        return None
        
    builder.button(text="« Назад", callback_data="back_to_main")
    builder.adjust(2, 1)
    
    return builder.as_markup()


def get_back_to_menu() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой возврата в главное меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="« Вернуться в главное меню", callback_data="back_to_main")
    return builder.as_markup()
    # Добавляем информационные кнопки
    builder.button(text="ℹ️ О компании/контакты", callback_data="about_company")
    builder.button(text="🤝 Сотрудничество", callback_data="cooperation")
    
    # Располагаем кнопки по 2 в ряду
    builder.adjust(2, 2, 2, 2, 1, 1)
    
    return builder.as_markup()


def get_subcategory_menu(category_slug: str) -> InlineKeyboardMarkup:
    """Создает меню подкатегорий"""
    builder = InlineKeyboardBuilder()
    
    with get_session() as session:
        # Находим родительскую категорию
        from database.db import get_category_by_slug
        parent_category = get_category_by_slug(session, category_slug)
        if not parent_category:
            return get_back_to_menu()
        
        # Получаем подкатегории
        subcategories = list_categories(session, parent_id=parent_category.id)
        
        if subcategories:
            # Добавляем подкатегории
            for subcategory in subcategories:
                builder.button(text=subcategory.name, callback_data=f"subcategory:{subcategory.slug}")
            
            # Проверяем, есть ли товары в родительской категории
            from database.db import list_products
            products_in_parent = list_products(session, category_id=parent_category.id)
            if products_in_parent:
                builder.button(text="📦 Все товары", callback_data=f"products:{category_slug}")
        else:
            # Если подкатегорий нет, показываем товары
            from database.db import list_products
            products = list_products(session, category_id=parent_category.id)
            if products:
                builder.button(text="📦 Показать товары", callback_data=f"products:{category_slug}")
    
    # Кнопка назад
    builder.button(text="⬅️ Назад", callback_data="main_menu")
    
    # Располагаем кнопки по 2 в ряду
    builder.adjust(2, 1)
    
    return builder.as_markup()


def get_products_menu(category_slug: str, page: int = 0, limit: int = 5) -> InlineKeyboardMarkup:
    """Создает меню товаров с пагинацией"""
    builder = InlineKeyboardBuilder()
    
    with get_session() as session:
        from database.db import get_category_by_slug, list_products
        category = get_category_by_slug(session, category_slug)
        if not category:
            return get_back_to_menu()
        
        products = list_products(session, category_id=category.id)
        
        # Показываем товары на текущей странице
        start_idx = page * limit
        end_idx = start_idx + limit
        page_products = products[start_idx:end_idx]
        
        for product in page_products:
            builder.button(
                text=f"📦 {product.title[:30]}{'...' if len(product.title) > 30 else ''}", 
                callback_data=f"product:{product.id}"
            )
        
        # Кнопки навигации
        if page > 0:
            builder.button(text="⬅️ Предыдущая", callback_data=f"products:{category_slug}:{page-1}")
        
        if end_idx < len(products):
            builder.button(text="➡️ Следующая", callback_data=f"products:{category_slug}:{page+1}")
        
        # Кнопка назад
        if category.parent_id:
            # Если это подкатегория, возвращаемся к подкатегориям
            builder.button(text="⬅️ Назад", callback_data=f"category:{category_slug}")
        else:
            # Если это основная категория, возвращаемся к подкатегориям
            builder.button(text="⬅️ Назад", callback_data=f"category:{category_slug}")
    
    # Располагаем кнопки по 1 в ряду
    builder.adjust(1)
    
    return builder.as_markup()


def get_back_to_menu() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    return builder.as_markup()


def get_back_button(callback_data: str) -> InlineKeyboardMarkup:
    """Кнопка назад с указанным callback_data"""
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data=callback_data)
    return builder.as_markup()