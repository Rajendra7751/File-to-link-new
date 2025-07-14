from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_link_buttons(links: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("▶️ Stream Now", url=links['stream_link']),
            InlineKeyboardButton("⬇️ Download", url=links['download_link'])
        ]
    ])

def format_size(size_bytes: int) -> str:
    # Convert file size to human-readable format
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    p = 1024
    while size_bytes >= p and i < len(size_name) - 1:
        size_bytes /= p
        i += 1
    return f"{round(size_bytes, 2)} {size_name[i]}"
