import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage

# ----------------- Настройки -----------------
BOT_TOKEN = "8512847602:AAFNT7FQGX8tu1ACELL9pI-LriKwhxob-B4"
ADMIN_CHAT_ID = -1003108483615
PAYMENT_URL = "https://example.com/pay?amount=50"
CHANNEL_INVITE_LINK = "https://t.me/+99IgL1KA_rhkYmZi"
VIDEO_URL = "https://www.youtube.com/watch?v=P-3NZnicpbk&feature=youtu.be"
MANUAL_PATH = os.path.join(os.path.dirname(__file__), "marketing_manual.pdf")
# ---------------------------------------------

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM состояния
class Flow(StatesGroup):
    landed = State()
    viewed = State()
    finished = State()


# Таймер спец-предложения (5 секунд для теста)
async def schedule_offer(chat_id: int, delay_seconds: int = None):
    if delay_seconds is None:
        delay_seconds = random.randint(40*60, 60*60)  # обычное поведение: 40-60 мин
    await asyncio.sleep(delay_seconds)
    await send_special_offer(chat_id)


async def send_special_offer(chat_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оформить подписку со скидкой 50%", url=PAYMENT_URL)]
    ])
    await bot.send_message(chat_id, (
        "🔥 Специальное предложение — только для тебя!\n\n"
        "Индивидуальная **скидка 50%** на доступ в закрытый канал Foton Plus.\n\n"
        "После оплаты сразу приходит ссылка на канал."
    ), reply_markup=keyboard)


# === /start ===
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Flow.landed)
    text = (
        "🔥 Привет! Ты попал(а) в спец-воронку Foton Plus.\n\n"
        "У нас есть **закрытый канал по маркетингу**, где мы делимся фишками и приёмами, "
        "которых нет в открытом доступе — рабочие воронки, шаблоны, кейсы.\n\n"
        "Как бонус — можешь сразу получить короткое обучающее видео «Запуск первой рекламы» и мини-мануал."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Получить бонус (видео + мануал)", callback_data="get_bonus")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")


# === Получение бонуса ===
@dp.callback_query(lambda c: c.data == "get_bonus")
async def cb_get_bonus(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    # Отправка мануала
    if os.path.exists(MANUAL_PATH):
        try:
            doc = FSInputFile(MANUAL_PATH)
            await callback.message.answer_document(document=doc, caption="📘 Мини-мануал — бонус к видео")
        except Exception as e:
            await callback.message.answer("❌ Не удалось отправить мануал.")
            print("send manual error:", e)
    else:
        await callback.message.answer("❌ Файл мануала не найден на сервере.")

    # Видео
    await callback.message.answer(f"🎥 Смотри видео: {VIDEO_URL}\n\nПриятного просмотра!", disable_web_page_preview=False)

    await state.set_state(Flow.viewed)

    # Планируем оффер через таймер 40-60 минут (тестовый режим можно с ключевым словом)
    asyncio.create_task(schedule_offer(callback.from_user.id))

    # Уведомляем админа
    try:
        await bot.send_message(ADMIN_CHAT_ID,
            f"🟢 Бонус выдан пользователю\n👤 @{callback.from_user.username or callback.from_user.full_name}\nID: {callback.from_user.id}"
        )
    except Exception:
        pass


# === Ловим секретные слова от админа ===
@dp.message()
async def admin_commands(message: types.Message):
    text = message.text.strip()
    user_id = message.from_user.id

    # Слово для мгновенного спец-предложения
    if text.upper() == "ЖОПА":
        await send_special_offer(user_id)
        await message.answer("✅ Тест: спец-предложение выдано мгновенно.")

    # Слово для мгновенной выдачи ссылки на канал (оплата)
    elif text.upper() == "ХУЙ":
        await message.answer(f"🎉 Тест: Вот приглашение в канал:\n\n{CHANNEL_INVITE_LINK}")
        await bot.send_message(ADMIN_CHAT_ID,
            f"💰 Тестовая оплата подтверждена пользователем @{message.from_user.username or message.from_user.full_name}\nID: {user_id}"
        )


# === Запуск бота ===
async def main():
    print("🤖 Бот запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
