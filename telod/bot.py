from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    filters,
    Updater,
)
from telod.models import Medicine, MedicineName
from asgiref.sync import sync_to_async
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def help_text() -> str:
    return (
        "Этот бот проверяет препараты на потенциальное отношение к фармакологической группе «фуфломицины»\n\n"
        "Если бот не находит лекарство в базе, значит есть вероятность того, что оно работает\n"
        "Если находит - значит с ним что-то не так. "
        "Список сформирован на основе отсутствия убедительных данных об эффективности препаратов по заявленным показаниям, "
        "как того требуют международные принципы доказательной медицины или по отсутствию в авторитетных источниках и рекомендациях\n\n"
        "Информация взята с сайта https://encyclopatia.ru/wiki/Расстрельный_список_препаратов"
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(f"Привет!\n\n{help_text()}")


async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(help_text())


def medicine_text(medicine: Medicine, search_name: str) -> str:
    text_parts: list[str] = []

    text_parts.append(f"Название: <strong>{search_name}</strong>")
    text_parts.append(f"\nОписание: {medicine.description}")

    return "\n".join(text_parts)


async def get_medicine_info(update: Update, context: CallbackContext) -> None:
    """Fetch medicine information based on the user's message."""
    query = update.message.text.strip()

    try:
        medicine_name = await sync_to_async(MedicineName.objects.get)(
            name__iexact=query
        )
        medicine = await sync_to_async(lambda: medicine_name.medicine)()
        medicine_info = medicine_text(medicine, query)
    except MedicineName.DoesNotExist:
        medicine_info = f"По вашему запросу <em>{query}</em> ничего не найдено"

    await update.message.reply_html(medicine_info, disable_web_page_preview=True)


def run_bot():
    """Set up and run the Telegram bot."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_medicine_info))

    app.run_polling()
