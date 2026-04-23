from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("8692752593:AAHu8clFlKmwd1bg7ZJtFzd2Jdm4d6O_NdU")

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Quick Match", callback_data="quick")],
        [InlineKeyboardButton("👥 Buat Room", callback_data="create")]
    ]

    await update.message.reply_text(
        "🎮 Sambung Kata",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "quick":
        await query.edit_message_text("⏳ Mencari lawan...")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
