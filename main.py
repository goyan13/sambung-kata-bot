from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random, string

TOKEN = "8692752593:AAHu8clFlKmwd1bg7ZJtFzd2Jdm4d6O_NdU"

app = ApplicationBuilder().token(TOKEN).build()

rooms = {}
user_state = {}

# =========================
# UTIL
# =========================
def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_player_list_text(room_id):
    players = rooms[room_id]["players"]
    text = ""
    for i, p in enumerate(players):
        text += f"{i+1}. {p}\n"
    return text

# =========================
# START MENU
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Quick Match", callback_data="quick")],
        [InlineKeyboardButton("👥 Buat Room", callback_data="create")],
        [InlineKeyboardButton("🔗 Join Room", callback_data="join")]
    ]
    await update.message.reply_text(
        "🎮 Sambung Kata\n\nPilih mode:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# BUTTON HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "create":
        keyboard = [
            [InlineKeyboardButton("👤 1v1", callback_data="mode_1v1")],
            [InlineKeyboardButton("👥 1v4", callback_data="mode_1v4")]
        ]
        await query.edit_message_text("Pilih mode:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("mode_"):
        mode = data.split("_")[1]
        room_id = generate_room_id()

        rooms[room_id] = {
            "host": user_id,
            "players": [user_id],
            "mode": mode
        }

        keyboard = [
            [InlineKeyboardButton("▶️ Mulai", callback_data=f"start_{room_id}")],
            [InlineKeyboardButton("❌ Keluar", callback_data=f"leave_{room_id}")]
        ]

        await query.edit_message_text(
            f"🎮 Room dibuat!\n\nID: {room_id}\n\nPlayer:\n1. Kamu (Host)",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "join":
        user_state[user_id] = "waiting_room"
        await query.edit_message_text("Masukkan Room ID:")

    elif data.startswith("start_"):
        room_id = data.split("_")[1]

        if rooms[room_id]["host"] != user_id:
            await query.answer("Hanya host!", show_alert=True)
            return

        await query.edit_message_text(f"🚀 Game dimulai!\nRoom: {room_id}")

    elif data.startswith("leave_"):
        room_id = data.split("_")[1]

        if room_id in rooms:
            if user_id in rooms[room_id]["players"]:
                rooms[room_id]["players"].remove(user_id)

        await query.edit_message_text("Kamu keluar dari room")

# =========================
# HANDLE TEXT (JOIN ROOM)
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.upper()

    if user_state.get(user_id) == "waiting_room":
        if text in rooms:
            rooms[text]["players"].append(user_id)

            await update.message.reply_text(
                f"✅ Masuk room {text}\n\nPlayer:\n{get_player_list_text(text)}"
            )
        else:
            await update.message.reply_text("❌ Room tidak ditemukan")

        user_state[user_id] = None

# =========================
# REGISTER
# =========================
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()