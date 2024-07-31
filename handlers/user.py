from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from fluentogram import TranslatorRunner

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


# Хендлер срабатывает на нажатие инлайн кнопки
@user_router.callback_query(F.data == 'button_pressed')
async def process_callback_query(callback: CallbackQuery, i18n: TranslatorRunner):
    await callback.answer(text=i18n.button.pressed())
