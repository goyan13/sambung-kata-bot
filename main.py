from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("8692752593:AAEpYKR7opjqlsBvtFsGIZKP-V4TYjTJXcc")

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Quick Match", callback_data="quick")],
        [InlineKeyboardButton("👥 Buat Room", callback_data="create")]
    ]

    await update.message.reply_text(
        "🎮 Sambung Kata\n\nPilih mode:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "quick":
        await query.edit_message_text("⏳ Mencari lawan...")

    elif query.data == "create":
        await query.edit_message_text("👥 Mode room (next step)")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
