from aiogram.fsm.state import State, StatesGroup


class OrderForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_comment = State()


class ConsultationForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_question = State()


class QuestionForm(StatesGroup):
    waiting_for_question = State()