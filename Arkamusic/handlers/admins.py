from asyncio import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message

from .. import queues
from ..Arkamusic import Arkamusic
from ..helpers.chat_id import get_chat_id
from ..helpers.decorators import authorized_users_only
from ..helpers.decorators import errors
from ..helpers.filters import command
from ..helpers.filters import other_filters


@Client.on_message(command('pause') & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    (
        await message.reply_text('<b>⏸ Paused</b>', False)
    ) if (
        Arkamusic.pause(get_chat_id(message.chat))
    ) else (
        await message.reply_text('<b>❌ Nothing is playing</b>', False)
    )


@Client.on_message(command('resume') & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    (
        await message.reply_text('<b>▶️ Resumed</b>', False)
    ) if (
        Arkamusic.resume(get_chat_id(message.chat))
    ) else (
        await message.reply_text('<b>❌ Nothing is paused</b>', False)
    )


@Client.on_message(command('stop') & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in Arkamusic.active_chats:
        await message.reply_text('<b>❌ Nothing is playing</b>', False)
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass
        await Arkamusic.stop(chat_id)
        await message.reply_text('<b>⏹ Stopped streaming</b>', False)


@Client.on_message(command('skip') & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in Arkamusic.active_chats:
        await message.reply_text('<b>❌ Nothing is playing</b>', False)
    else:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await Arkamusic.stop(chat_id)
        else:
            await Arkamusic.set_stream(
                chat_id,
                queues.get(chat_id)['file'],
            )
        await message.reply_text('<b>✅ Skipped</b>', False)


@Client.on_message(command('mute') & other_filters)
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = Arkamusic.mute(get_chat_id(message.chat))
    (
        await message.reply_text('<b>✅ Muted</b>', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('<b>❌ Already muted</b>', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('<b>❌ Not in call</b>', False)
    )


@Client.on_message(command('unmute') & other_filters)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = Arkamusic.unmute(get_chat_id(message.chat))
    (
        await message.reply_text('<b>✅ Unmuted</b>', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('<b>❌ Not muted</b>', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('<b>❌ Not in call</b>', False)
    )
