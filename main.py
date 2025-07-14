import asyncio
from pyrogram import Client
from aiohttp import web

from app.config import Config
from app.server import web_server
from app.handlers import *  # ✅ This is required to load your /start and file handlers

# ✅ In-memory session to avoid Render's file system lock issues
bot = Client(
    name=":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="/tmp"
)

async def main():
    await bot.start()
    print(f"✅ Bot @{(await bot.get_me()).username} started!")

    # 🌐 Start aiohttp web server
    app = await web_server(Config.BOT_TOKEN)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", Config.PORT)
    await site.start()
    print(f"🌐 Web server running at http://0.0.0.0:{Config.PORT}")

    # 🚀 Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
