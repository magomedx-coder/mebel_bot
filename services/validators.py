import re
from typing import Optional


def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    # Убираем все символы кроме цифр и +
    clean_phone = re.sub(r'[^\d+]', '', phone)
    
    # Проверяем российские номера
    russian_patterns = [
        r'^\+7\d{10}$',  # +7XXXXXXXXXX
        r'^7\d{10}$',    # 7XXXXXXXXXX
        r'^8\d{10}$',    # 8XXXXXXXXXX
        r'^\d{10}$',     # XXXXXXXXXX
    ]
    
    for pattern in russian_patterns:
        if re.match(pattern, clean_phone):
            return True
    
    return False


def format_phone(phone: str) -> str:
    """Форматирование номера телефона"""
    clean_phone = re.sub(r'[^\d+]', '', phone)
    
    if clean_phone.startswith('+7'):
        return clean_phone
    elif clean_phone.startswith('7'):
        return '+' + clean_phone
    elif clean_phone.startswith('8'):
        return '+7' + clean_phone[1:]
    elif len(clean_phone) == 10:
        return '+7' + clean_phone
    else:
        return clean_phone


def validate_name(name: str) -> bool:
    """Валидация имени"""
    if not name or len(name.strip()) < 2:
        return False
    
    # Проверяем, что имя содержит только буквы, пробелы и дефисы
    if not re.match(r'^[а-яёА-ЯЁa-zA-Z\s\-]+$', name.strip()):
        return False
    
    return True


def validate_text(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Валидация текста"""
    if not text or len(text.strip()) < min_length:
        return False
    
    if len(text.strip()) > max_length:
        return False
    
    return True