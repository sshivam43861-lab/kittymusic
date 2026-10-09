

# ==========================================================
# Copyright (c) 2026 ArtistBots
# All Rights Reserved.
# ==========================================================

import re

from pyrogram import enums, errors, filters, types

from Elevenyts import app, config, db, lang
from Elevenyts.helpers import buttons, utils


def parse_custom_emojis(text):
    pattern = re.compile(r'<emoji id="(\d+)">(.*?)</emoji>')
    entities = []
    parts = []
    cursor = 0
    offset = 0

    for match in pattern.finditer(text):
        before = text[cursor:match.start()]
        parts.append(before)
        offset += len(before.encode("utf-16-le")) // 2

        emoji_id = match.group(1)
        emoji = match.group(2)
        parts.append(emoji)

        entities.append(
            types.MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset,
                length=len(emoji.encode("utf-16-le")) // 2,
                custom_emoji_id=emoji_id,
            )
        )

        offset += len(emoji.encode("utf-16-le")) // 2
        cursor = match.end()

    parts.append(text[cursor:])
    return "".join(parts), entities


@app.on_message(filters.document & filters.private)
async def get_gif_id(_, message):
    if not message.document.file_name.lower().endswith(".gif"):
        return

    path = await message.download()
    sent = await message.reply_animation(animation=path)

    await message.reply_text(
        f"Animation File ID:\n`{sent.animation.file_id}`"
    )


@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    try:
        await m.reply_animation(
            animation=config.START_IMG,
            caption=m.lang["help_menu"],
            reply_markup=buttons.help_markup(m.lang),
            parse_mode=enums.ParseMode.HTML,
        )
    except Exception:
        await m.reply_text(
            text=m.lang["help_menu"],
            reply_markup=buttons.help_markup(m.lang),
            parse_mode=enums.ParseMode.HTML,
        )


@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    if message.chat.type != enums.ChatType.PRIVATE:
        try:
            await message.delete()
        except Exception:
            pass

    if not message.from_user:
        return

    if (
        message.from_user.id in app.bl_users
        and message.from_user.id not in db.notified
    ):
        return await message.reply_text(message.lang["bl_user_notify"])

    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    private = message.chat.type == enums.ChatType.PRIVATE

    if private:
        _text = message.lang["start_pm"].format(
            message.from_user.first_name, app.name
        )
        _text, entities = parse_custom_emojis(_text)
    else:
        _text = message.lang["start_gp"].format(app.name)
        entities = None

    key = buttons.start_key(message.lang, private)

    try:
        await message.reply_animation(
            animation=config.START_IMG,
            caption=_text,
            caption_entities=entities,
            reply_markup=key,
        )
    except Exception:
        await message.reply_text(
            text=_text,
            entities=entities,
            reply_markup=key,
        )

    if private:
        if await db.is_user(message.from_user.id):
            return

        await utils.send_log(message)
        return await db.add_user(message.from_user.id)


@app.on_message(
    filters.command(["playmode", "settings"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
async def settings(_, message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass

    admin_only = await db.get_play_mode(message.chat.id)
    _language = "en"

    await utils.safe_text(
        message,
        message.lang["start_settings"].format(message.chat.title),
        reply_markup=buttons.settings_markup(
            message.lang, admin_only, _language, message.chat.id
        ),
        quote=True,
    )


@app.on_message(filters.new_chat_members, group=7)
@lang.language()
async def _new_member(_, message: types.Message):
    if message.chat.type != enums.ChatType.SUPERGROUP:
        return await message.chat.leave()

    for member in message.new_chat_members:
        if member.id == app.id:
            if await db.is_chat(message.chat.id):
                return

            await db.add_chat(message.chat.id)
