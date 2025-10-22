from aiogram.fsm.state import State, StatesGroup


class AdminAuth(StatesGroup):
    """Состояния для авторизации администратора"""
    waiting_for_password = State()


class CategoryForm(StatesGroup):
    """Состояния формы добавления категории"""
    waiting_for_name = State()
    waiting_for_slug = State()
    waiting_for_description = State()


class FurnitureForm(StatesGroup):
    """Состояния формы добавления мебели"""
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_description = State()
    waiting_for_dimensions = State()
    waiting_for_material = State()
    waiting_for_photo = State()
    waiting_for_origin = State()  # Для мебели из России/Турции
    waiting_for_kitchen_type = State()  # Для типов кухонь (прямая/угловая)