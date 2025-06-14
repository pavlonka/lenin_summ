from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

# Загрузка пайплайна суммаризации
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Можно выбрать другую модель

# Ваш токен бота
TELEGRAM_TOKEN = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне текст, и я кратко его перескажу.")

async def summarize_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    # Ограничение на длину входа для BART — 1024 токена (~1000-1500 слов)
    if len(input_text) > 3500:
        await update.message.reply_text("Текст слишком длинный! Пожалуйста, отправьте текст поменьше.")
        return
    summary = summarizer(input_text, min_length=30, max_length=150)[0]["summary_text"]
    await update.message.reply_text(f"Суммаризация:\n{summary}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, summarize_text))
    app.run_polling()
