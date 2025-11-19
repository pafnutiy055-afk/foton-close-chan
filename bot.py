import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatAction, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

# --- КОНФИГУРАЦИЯ ---
# В реальном проекте лучше использовать os.getenv("BOT_TOKEN") и файл .env
BOT_TOKEN = "8324054424:AAFsS1eHNEom5XpTO3dM2U-NdFIaVkZERX0"
NOTIFY_CHAT_ID = -1003322951241
MANAGER_LINK = "https://t.me/bery_lydu"

# Файлы (убедись, что они лежат рядом с файлом бота)
FILES = {
    "manual": "marketing_manual.pdf",
    "kpi": "metrika.pdf",
    "checklist": "check_list.pdf"
}

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

# --- ТЕКСТЫ (Вынесены отдельно для удобства правки) ---
class Texts:
    WELCOME = (
        "👋 **Привет! Это Артём и команда Foton Plus.**\n\n"
        "Мы не льем воду, мы даем инструменты, которые приносят деньги. 💸\n"
        "Я подготовил для тебя пошаговую систему по маркетингу.\n\n"
        "Готов забрать первый инструмент и усилить свой бизнес? 👇"
    )
    MANUAL_SENT = (
        "📘 **Твой Мануал по маркетингу**\n\n"
        "Изучи его, чтобы понимать базу. Но теория без цифр — ничто.\n"
        "Готов взять под контроль показатели своего бизнеса?"
    )
    KPI_SENT = (
        "📊 **Таблица KPI (Метрика)**\n\n"
        "Теперь ты видишь цифры. Но уверен ли ты, что твоя реклама настроена без ошибок?\n"
        "Держи чек-лист, который спас тысячи бюджетов от слива. 👇"
    )
    CHECKLIST_SENT = (
        "📑 **Чек-лист «Проверка кампании»**\n\n"
        "Теперь ты защищен от глупых ошибок. \n"
        "🔥 А сейчас — самое главное. **Секретный видеоурок**, где я разбираю реальные стратегии."
    )
    VIDEO_SENT = (
        "🎥 **ДОСТУП ОТКРЫТ!**\n\n"
        "В этом видео — концентрат опыта. Смотри внимательно, инсайты гарантированы.\n\n"
        "⏳ *Через 2 часа я вернусь с важным предложением.*"
    )
    QUIZ_OFFER = (
        "🚀 **Прошло 2 часа! Как впечатления?**\n\n"
        "Материалы — это круто, но результат дает только **индивидуальная стратегия**.\n\n"
        "Давай я помогу адаптировать эти знания под ТВОЙ бизнес. \n"
        "Ответь на 4 простых вопроса, и мы составим план действий конкретно для тебя. 👇"
    )
    QUIZ_FINAL = (
        "🔥 **Спасибо! Я проанализировал твои ответы.**\n\n"
        "Мы подготовили стратегию специально под твою нишу.\n"
        "Нажми кнопку ниже, напиши менеджеру **«РАЗБОР»**, и мы бесплатно обсудим твой запуск! 👇"
    )

# --- МАШИНА СОСТОЯНИЙ (FSM) ---
class QuizStates(StatesGroup):
    niche = State()
    goal = State()
    experience = State()
    platform = State()

# --- ИНИЦИАЛИЗАЦИЯ ---
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
storage = MemoryStorage() # Для продакшена лучше использовать RedisStorage
dp = Dispatcher(storage=storage)

# --- УТИЛИТЫ ---
async def simulate_typing(chat_id: int, sleep_time: float = 1.0):
    """Имитирует набор текста ботом."""
    try:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await asyncio.sleep(sleep_time)
    except Exception as e:
        logger.error(f"Ошибка в simulate_typing: {e}")

def get_user_link(user: types.User) -> str:
    """Возвращает username или имя с ссылкой."""
    return f"@{user.username}" if user.username else f"[{user.full_name}](tg://user?id={user.id})"

# --- ХЕНДЛЕРЫ ВОРОНКИ ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await simulate_typing(message.chat.id, 0.5)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="📘 Скачать мануал", callback_data="get_manual")
    
    await message.answer(Texts.WELCOME, reply_markup=kb.as_markup())
    
    try:
        await bot.send_message(NOTIFY_CHAT_ID, f"🔥 Новый лид: {get_user_link(message.from_user)} (ID: {message.from_user.id})", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Ошибка уведомления о старте: {e}")

@dp.callback_query(F.data == "get_manual")
async def send_manual(callback: types.CallbackQuery):
    await callback.answer()
    await simulate_typing(callback.message.chat.id, 0.5)

    if os.path.exists(FILES["manual"]):
        await callback.message.answer_document(FSInputFile(FILES["manual"]), caption="📘 Твой мануал")
    else:
        await callback.message.answer("⚠️ Файл временно недоступен.")
        logger.warning(f"Файл {FILES['manual']} не найден!")

    await simulate_typing(callback.message.chat.id, 0.7)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Забрать таблицу KPI", callback_data="get_kpi")
    
    await callback.message.answer(Texts.MANUAL_SENT, reply_markup=kb.as_markup())

@dp.callback_query(F.data == "get_kpi")
async def send_kpi(callback: types.CallbackQuery):
    await callback.answer()
    await simulate_typing(callback.message.chat.id, 0.5)

    if os.path.exists(FILES["kpi"]):
        await callback.message.answer_document(FSInputFile(FILES["kpi"]), caption="📊 Таблица KPI")
    else:
        await callback.message.answer("⚠️ Файл временно недоступен.")

    await simulate_typing(callback.message.chat.id, 0.7)

    kb = InlineKeyboardBuilder()
    kb.button(text="📑 Получить чек-лист", callback_data="get_checklist")
    
    await callback.message.answer(Texts.KPI_SENT, reply_markup=kb.as_markup())

@dp.callback_query(F.data == "get_checklist")
async def send_checklist(callback: types.CallbackQuery):
    await callback.answer()
    await simulate_typing(callback.message.chat.id, 0.5)
    
    if os.path.exists(FILES["checklist"]):
        await callback.message.answer_document(FSInputFile(FILES["checklist"]), caption="📑 Чек-лист")
    else:
        await callback.message.answer("⚠️ Файл временно недоступен.")

    await simulate_typing(callback.message.chat.id, 0.8)

    kb = InlineKeyboardBuilder()
    kb.button(text="🎥 Смотреть видеоурок", callback_data="get_video")
    
    await callback.message.answer(Texts.CHECKLIST_SENT, reply_markup=kb.as_markup())

@dp.callback_query(F.data == "get_video")
async def send_video(callback: types.CallbackQuery):
    await callback.answer()
    await simulate_typing(callback.message.chat.id, 1.0)
    
    VIDEO_URL = "https://youtu.be/P-3NZnicpbk"
    kb = InlineKeyboardBuilder()
    kb.button(text="▶️ СМОТРЕТЬ УРОК", url=VIDEO_URL)
    
    await callback.message.answer(Texts.VIDEO_SENT, reply_markup=kb.as_markup())

    await bot.send_message(NOTIFY_CHAT_ID, f"🎬 Лид смотрит видео: {get_user_link(callback.from_user)}", parse_mode="Markdown")

    # Запускаем таймер. 
    # ВАЖНО: Если бот перезагрузится, таймер сбросится. 
    # Для надежности в проде используются Celery или планировщики БД.
    asyncio.create_task(delayed_quiz_offer(callback.message.chat.id))

async def delayed_quiz_offer(chat_id: int):
    """Отложенная отправка оффера на квиз."""
    await asyncio.sleep(2 * 60 * 60) # 2 часа
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🧠 ПРОЙТИ РАЗБОР", callback_data="start_quiz")
    
    try:
        await bot.send_message(chat_id, Texts.QUIZ_OFFER, reply_markup=kb.as_markup())
    except Exception as e:
        logger.warning(f"Не удалось отправить отложенное сообщение (юзер мог заблокировать бота): {e}")

# --- ХЕНДЛЕРЫ КВИЗА (С ИСПОЛЬЗОВАНИЕМ FSM) ---

@dp.callback_query(F.data == "start_quiz")
async def quiz_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await simulate_typing(callback.message.chat.id, 0.5)

    await callback.message.answer("1️⃣ **Вопрос 1:** В какой нише вы работаете?")
    await state.set_state(QuizStates.niche)
    
    await bot.send_message(NOTIFY_CHAT_ID, f"🧠 Лид начал квиз: {get_user_link(callback.from_user)}", parse_mode="Markdown")

@dp.message(StateFilter(QuizStates.niche))
async def quiz_niche(message: types.Message, state: FSMContext):
    await state.update_data(niche=message.text)
    await simulate_typing(message.chat.id, 0.7)
    
    await message.answer("2️⃣ **Вопрос 2:** Какая ГЛАВНАЯ цель вашей рекламы сейчас?")
    await state.set_state(QuizStates.goal)

@dp.message(StateFilter(QuizStates.goal))
async def quiz_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await simulate_typing(message.chat.id, 0.7)
    
    # Здесь можно добавить кнопки для выбора варианта, но оставим текст как в оригинале
    await message.answer("3️⃣ **Вопрос 3:** Какой у вас опыт в рекламе? (Новичок / Сливал бюджет / Профи)")
    await state.set_state(QuizStates.experience)

@dp.message(StateFilter(QuizStates.experience))
async def quiz_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await simulate_typing(message.chat.id, 0.7)
    
    await message.answer("4️⃣ **Вопрос 4:** На какой площадке планируете запускаться? (VK / Яндекс / Telegram / Другое)")
    await state.set_state(QuizStates.platform)

@dp.message(StateFilter(QuizStates.platform))
async def quiz_finish(message: types.Message, state: FSMContext):
    # Сохраняем последний ответ
    await state.update_data(platform=message.text)
    
    # Получаем все данные
    data = await state.get_data()
    await state.clear() # Очищаем состояние
    
    # Отправка заявки
    answers = (
        f"🔹 **Ниша:** {data.get('niche')}\n"
        f"🔹 **Цель:** {data.get('goal')}\n"
        f"🔹 **Опыт:** {data.get('experience')}\n"
        f"🔹 **Площадка:** {data.get('platform')}"
    )

    await bot.send_message(
        NOTIFY_CHAT_ID, 
        f"✅ **КВИЗ ЗАВЕРШЕН!**\n👤: {get_user_link(message.from_user)}\n\n📄 **Ответы:**\n{answers}",
        parse_mode="Markdown"
    )

    # Ответ пользователю
    await simulate_typing(message.chat.id, 1.0)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="📩 ЗАБРАТЬ РАЗБОР", url=MANAGER_LINK)

    await message.answer(Texts.QUIZ_FINAL, reply_markup=kb.as_markup())

# --- ЗАПУСК ---
async def main():
    logger.info("Бот запущен и готов к работе...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
