from aiohttp import web
from pyrogram import Client
from app.config import Config
import os

routes = web.RouteTableDef()

DOWNLOAD_DIR = "downloads"

# Helper: download file from Telegram if not already stored
async def download_file(file_id: str, file_path: str):
    client = Client(
        name="downloader",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        workdir="/tmp"
    )
    async with client:
        await client.download_media(file_id, file_name=file_path)

# Download endpoint
@routes.get("/download/{file_id}/{file_name}")
async def download_handler(request):
    file_id = request.match_info["file_id"]
    file_name = request.match_info["file_name"]
    file_path = f"{DOWNLOAD_DIR}/{file_name}"

    if not os.path.exists(file_path):
        try:
            await download_file(file_id, file_path)
        except Exception as e:
            return web.Response(text=f"❌ Error downloading file: {e}", status=500)

    if os.path.exists(file_path):
        return web.FileResponse(path=file_path)
    return web.Response(text="❌ File not found.", status=404)

# Stream endpoint
@routes.get("/stream/{file_id}/{file_name}")
async def stream_handler(request):
    file_id = request.match_info["file_id"]
    file_name = request.match_info["file_name"]
    file_path = f"{DOWNLOAD_DIR}/{file_name}"

    if not os.path.exists(file_path):
        try:
            await download_file(file_id, file_path)
        except Exception as e:
            return web.Response(text=f"❌ Error preparing stream: {e}", status=500)

    if os.path.exists(file_path):
        return web.FileResponse(path=file_path)
    return web.Response(text="❌ Stream not available.", status=404)

# Return aiohttp app
async def web_server(token: str):
    app = web.Application()
    app.add_routes(routes)
    return app
