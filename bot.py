import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from instagrapi import Client

# Load environment
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Env variables
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))
MONGO_URI = os.getenv("MONGO_URI")

# Mongo setup
mongo = MongoClient(MONGO_URI)
db = mongo["telegram_bot"]
settings_collection = db["settings"]

# IG client
def get_ig_client():
    creds = settings_collection.find_one({"_id": "instagram"})
    if not creds or not creds.get("username") or not creds.get("password"):
        raise Exception("Instagram credentials not set.")
    cl = Client()
    cl.login(creds["username"], creds["password"])
    return cl

# Owner check
def owner_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != BOT_OWNER_ID:
            await update.message.reply_text("❌ You are not authorized.")
            return
        return await func(update, context)
    return wrapper

# Start command (public)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Instagram Reels Uploader Bot!")

# Upload command (owner only)
@owner_only
async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a video/document to upload.")
        return

    reply = update.message.reply_to_message
    file_id = None

    if reply.video:
        file_id = reply.video.file_id
    elif reply.document and reply.document.mime_type.startswith("video/"):
        file_id = reply.document.file_id
    else:
        await update.message.reply_text("⚠️ The replied message is not a valid video.")
        return

    file = await context.bot.get_file(file_id)
    file_path = f"{reply.message_id}.mp4"
    await file.download_to_drive(file_path)
    await update.message.reply_text("⏳ Uploading...")

    try:
        cl = get_ig_client()
        caption = reply.caption or "Uploaded via Telegram Bot"
        cl.clip_upload(file_path, caption)
        await update.message.reply_text("✅ Uploaded successfully!")
        logger.info("Reel uploaded.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Upload failed: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Settings command (owner only)
@owner_only
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [["VIEW VARIABLE"], ["IG USERNAME", "IG PASSWORD"], ["CANCEL"]],
        resize_keyboard=True
    )
    await update.message.reply_text("⚙️ IG Settings:", reply_markup=keyboard)

@owner_only
async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "VIEW VARIABLE":
        creds = settings_collection.find_one({"_id": "instagram"}) or {}
        username = creds.get("username", "Not Set")
        password = creds.get("password", "Not Set")
        await update.message.reply_text(f"👤 Username: `{username}`\n🔑 Password: `{password}`", parse_mode="Markdown")
    elif text == "IG USERNAME":
        context.user_data["awaiting"] = "username"
        await update.message.reply_text("✏️ Send new IG username:")
    elif text == "IG PASSWORD":
        context.user_data["awaiting"] = "password"
        await update.message.reply_text("✏️ Send new IG password:")
    elif text == "CANCEL":
        context.user_data.pop("awaiting", None)
        await update.message.reply_text("❎ Cancelled.", reply_markup=ReplyKeyboardRemove())
    elif context.user_data.get("awaiting") == "username":
        settings_collection.update_one({"_id": "instagram"}, {"$set": {"username": text}}, upsert=True)
        context.user_data.pop("awaiting", None)
        await update.message.reply_text("✅ Username saved.")
    elif context.user_data.get("awaiting") == "password":
        settings_collection.update_one({"_id": "instagram"}, {"$set": {"password": text}}, upsert=True)
        context.user_data.pop("awaiting", None)
        await update.message.reply_text("✅ Password saved.")
    else:
        await update.message.reply_text("❓ Unknown command.")

# Cancel command (owner only)
@owner_only
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❎ Operation cancelled.", reply_markup=ReplyKeyboardRemove())

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("upload", upload_command))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, settings_handler))

    logger.info("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
