from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import get_main_menu, get_back_to_menu

router = Router()

WELCOME_TEXT = """🌟 Добро пожаловать в наш мебельный бот! 🌟

🛋️ Здесь вы найдете стильную и качественную мебель для любого интерьера.

📂 Наш каталог включает:
• Спальни и матрасы
• Кухонные гарнитуры
• Мягкую мебель
• Столы и стулья
• Тумбы и комоды
• Шкафы-купе и гардеробные

🛒 Как сделать заказ:
1. Выберите категорию мебели
2. Просмотрите модели
3. Свяжитесь с нами для заказа

💬 Для оформления заказа потребуется ваше имя и номер телефона
🔄 В любой момент можно вернуться в главное меню

👇 Выберите категорию из меню ниже:"""


@router.message(F.text == "/start")
async def start_command(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        text=WELCOME_TEXT,
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        text=WELCOME_TEXT,
        reply_markup=get_main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "about_company")
async def about_company(callback: CallbackQuery):
    """Информация о компании"""
    about_text = """🪑 О компании

Наша мастерская мебели — это команда профессионалов, создающих мебель с душой и вниманием к каждой детали. 
Мы изготавливаем широкий ассортимент изделий: корпусную, мягкую, кухонную, офисную и декоративную мебель под заказ.

✨ Мы работаем с натуральными и экологичными материалами, применяем современные технологии 
и гарантируем долговечность каждой модели. От простых минималистичных решений до дизайнерских проектов — 
мы воплощаем любые идеи, сохраняя баланс между эстетикой, комфортом и качеством.

📦 Что мы предлагаем:
• Индивидуальные проекты под размеры заказчика
• Большой выбор материалов и фурнитуры
• Гарантию 2 года на всю продукцию
• Быструю доставку по России и СНГ

💬 Хотите оформить заказ или обсудить проект? Мы всегда на связи!

📲 Связаться с нами:
WhatsApp: https://wa.me/+79370080708
Telegram: https://t.me/79370080708

🤖 Хотите заказать Telegram-бота или другое IT-решение?
Обращайтесь: https://instagram.com/movsarcoder"""
    
    await callback.message.edit_text(
        text=about_text,
        reply_markup=get_back_to_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "cooperation")
async def cooperation(callback: CallbackQuery):
    """Информация о сотрудничестве"""
    cooperation_text = """🤝 Сотрудничество

Мы открыты для сотрудничества с:
• Дизайнерами интерьеров
• Строительными компаниями
• Магазинами мебели
• Частными мастерами

💼 Условия сотрудничества:
• Специальные цены для партнеров
• Быстрые сроки изготовления
• Техническая поддержка
• Обучение персонала

📞 Для обсуждения условий сотрудничества:
WhatsApp: https://wa.me/+79370080708
Telegram: https://t.me/79370080708"""
    
    await callback.message.edit_text(
        text=cooperation_text,
        reply_markup=get_back_to_menu()
    )
    await callback.answer()

