from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from fluentogram import TranslatorRunner

from states.states import NatsTestSG

user_router = Router()

# Хендлер срабатывает на команду /start
@user_router.message(CommandStart())
async def process_start_command(message: Message, i18n: TranslatorRunner):
    username = html.quote(message.from_user.full_name)
    # Создаем объект инлайн кнопки
    button = InlineKeyboardButton(
        text=i18n.button.button(),
        callback_data='button_pressed'
    )
    # Создаем объект клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(
        text=i18n.hello.user(username=username),
        reply_markup=markup
    )


# Хендлер срабатывает на команду /update
@user_router.message(Command(commands='update'))
async def process_update_command(message: Message, i18n: TranslatorRunner, state: FSMContext):
    # Отправляем пользователю сообщение с предложением прислать любой текст
    await message.answer(text=i18n.send.text())
    # Устанавливаем состояние ожидания ввода текста
    await state.set_state(NatsTestSG.enter_text)


# Хендлер срабатывает на команду /read
@user_router.message(Command(commands='read'))
async def process_read_command(message: Message, state: FSMContext):
    # Получаем FSM data
    data = await state.get_data()
    # Отправляем в телеграм-клиент строковое представление FSM data
    await message.answer(text=str(data))


# Хендлер срабатывает на любой текст в состоянии 'NatsTestSG.enter_text'
@user_router.message(F.text, StateFilter(NatsTestSG.enter_text))
async def process_enter_text(message: Message, i18n: TranslatorRunner, state: FSMContext):
    # Обновляем FSM data
    await state.update_data(text=message.text)
    await message.answer(text=i18n.successfully.saved())
    await state.set_state()


# Хендлер срабатывает на любое нетекстовое сообщение в состоянии 'NatsTestSG.enter_text'
@user_router.message(StateFilter(NatsTestSG.enter_text))
async def process_any_message(message: Message, i18n: TranslatorRunner, state: FSMContext):
    await message.answer(text=i18n.text.only())


# Хендлер срабатывает на нажатие инлайн кнопки
@user_router.callback_query(F.data == 'button_pressed')
async def process_callback_query(callback: CallbackQuery, i18n: TranslatorRunner):
    await callback.answer(text=i18n.button.pressed())

