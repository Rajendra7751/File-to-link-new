import asyncio
from pyrogram import Client
from aiohttp import web

from app.config import Config
from app.server import web_server
import app.handlers  # Register handlers

# Pyrogram client setup
bot = Client(
    name="bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="/tmp"
)

async def main():
    try:
        print("🔁 Starting bot...")
        await bot.start()
        me = await bot.get_me()
        print(f"✅ Bot @{me.username} started!")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        return

    try:
        print("🌐 Starting web server...")
        app = await web_server(Config.BOT_TOKEN)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", Config.PORT)
        await site.start()
        print(f"🌐 Web server running at http://0.0.0.0:{Config.PORT}")
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        return

    # Keep running forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Main crashed: {e}")
