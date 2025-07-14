import asyncio
from pyrogram import Client
from aiohttp import web
from app.config import Config
#from app.handlers import setup_handlers
from app.server import web_server

bot = Client(
    name="FileToLinkBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

async def main():
    await bot.start()
    print(f"✅ Bot started as @{(await bot.get_me()).username}")

    setup_handlers(bot)

    app = await web_server(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", Config.PORT)
    await site.start()
    print(f"🌐 Web server started at http://0.0.0.0:{Config.PORT}")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
