import os

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_URI = os.getenv("DB_URI")
    BIN_CHANNEL = int(os.getenv("BIN_CHANNEL", "-1002569669378"))  # default fallback
    FQDN = os.getenv("FQDN", "localhost")
    PORT = int(os.getenv("PORT", "8080"))
    HAS_SSL = os.getenv("HAS_SSL", "False").lower() == "true"
    NO_PORT = os.getenv("NO_PORT", "False").lower() == "true"
