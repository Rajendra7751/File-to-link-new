from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.config import Config
import os
from pathlib import Path

# Create the downloads folder if it doesn't exist
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# /start command
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message: Message):
    await message.reply_text(
        "👋 Hello! Send me a file and I will generate a permanent download and stream link for you.\n\nJust upload the file here."
    )

# Handle private document (file) messages
@Client.on_message(filters.private & filters.document)
async def handle_file(bot, message: Message):
    downloading = await message.reply_text("📥 Downloading your file...")
    
    # Save file to downloads folder
    file_path = await bot.download_media(message, file_name=f"{DOWNLOAD_DIR}/{message.document.file_name}")
    await downloading.edit_text("✅ File saved, generating link...")

    # Extract file info
    file_id = message.document.file_id
    file_name = message.document.file_name

    # Generate base URL
    base_url = f"https://{Config.FQDN}" if Config.HAS_SSL else f"http://{Config.FQDN}"
    if not Config.NO_PORT:
        base_url += f":{Config.PORT}"

    # Generate final URLs
    stream_link = f"{base_url}/stream/{file_id}/{file_name}"
    download_link = f"{base_url}/download/{file_id}/{file_name}"

    # Send links with buttons
    buttons = [
        [
            InlineKeyboardButton("▶️ Stream", url=stream_link),
            InlineKeyboardButton("⬇️ Download", url=download_link)
        ]
    ]

    await message.reply_text(
        f"🎬 **File Name:** `{file_name}`\n📡 **Permanent Links Generated Below**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
