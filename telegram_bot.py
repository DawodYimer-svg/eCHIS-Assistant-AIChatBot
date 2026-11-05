import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

load_dotenv()
from src.rag import rag_chain

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm the eCHIS Assistant. Ask me a question about e-CHIS."
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.chat.send_action(ChatAction.TYPING)
    try:
        # rag_chain.invoke is blocking, so run it in a thread
        result = await asyncio.to_thread(rag_chain.invoke, {"input": question})
        reply = str(result["answer"])
    except Exception as e:
        print("Error:", e)
        reply = "Sorry, I can't answer right now. Please try again in a moment."

    # Telegram messages are limited to 4096 characters
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i:i + 4000])

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    print("Telegram bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()