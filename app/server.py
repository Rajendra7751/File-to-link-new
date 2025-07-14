from aiohttp import web
from pyrogram import Client
from app.config import Config
from pyrogram.errors import FloodWait
import asyncio
import aiofiles
import os

routes = web.RouteTableDef()

clients = {}

async def download_file(client: Client, file_id: str, file_path: str):
    async with client:
        await client.download_media(file_id, file_name=file_path)

@routes.get("/download/{file_id}/{file_name}")
async def download_handler(request):
    file_id = request.match_info['file_id']
    file_name = request.match_info['file_name']
    file_path = f"downloads/{file_name}"

    if not os.path.exists(file_path):
        client = Client(
            name="temp",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workdir="/tmp"
        )
        try:
            await download_file(client, file_id, file_path)
        except Exception as e:
            return web.Response(text="Error downloading file.", status=500)

    try:
        return web.FileResponse(path=file_path)
    except Exception as e:
        return web.Response(text="File not found.", status=404)

@routes.get("/stream/{file_id}/{file_name}")
async def stream_handler(request):
    file_id = request.match_info['file_id']
    file_name = request.match_info['file_name']
    file_path = f"downloads/{file_name}"

    if not os.path.exists(file_path):
        client = Client(
            name="temp",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workdir="/tmp"
        )
        try:
            await download_file(client, file_id, file_path)
        except Exception as e:
            return web.Response(text="Error downloading file.", status=500)

    try:
        return web.FileResponse(path=file_path)
    except Exception:
        return web.Response(text="Stream not available.", status=404)

async def web_server(token: str):
    app = web.Application()
    app.add_routes(routes)
    return app
