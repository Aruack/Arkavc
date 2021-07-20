from pyrogram import Client as Bot

from .Arkamusic import run
from .config import API_HASH
from .config import API_ID
from .config import BOT_TOKEN


Bot(
    ':memory:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Arkamusic.handlers'},
).start()
run()
