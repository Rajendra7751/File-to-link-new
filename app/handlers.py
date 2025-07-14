from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.config import Config
import os
import aiofiles
from pathlib import Path

# Create downloads folder if not exists
STREAM_PATH = Path("downloads")
STREAM_PATH.mkdir(exist_ok=True)

# /start handler
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message: Message):
    await message.reply_text(
        "👋 Hello! Send me a file and I will generate a permanent download and stream link for you.\n\nJust upload the file here."
    )

# Handle file upload and generate links
@Client.on_message(filters.private & filters.document)
async def save_file(bot, message: Message):
    downloading = await message.reply_text("📥 Downloading your file...")
    file_path = await bot.download_media(message, file_name=f"{STREAM_PATH}/{message.document.file_name}")
    await downloading.edit_text("✅ File saved, generating link...")

    file_id = message.document.file_id
    file_name = message.document.file_name
    base_url = f"https://{Config.FQDN}" if Config.HAS_SSL else f"http://{Config.FQDN}"
    if not Config.NO_PORT:
        base_url += f":{Config.PORT}"

    stream_url = f"{base_url}/stream/{file_id}/{file_name}"
    direct_url = f"{base_url}/download/{file_id}/{file_name}"

    buttons = [[
        InlineKeyboardButton("▶️ Stream", url=stream_url),
        InlineKeyboardButton("⬇️ Download", url=direct_url)
    ]]

    await message.reply_text(
        f"🎬 **File Name:** `{file_name}`\n📡 **Permanent Links Generated Below**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
