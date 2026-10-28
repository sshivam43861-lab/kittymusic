# ==========================================================
# Copyright (c) 2026 ArtistBots
# All Rights Reserved.
#
# Project      : ArtistBots API Telegram Music Bot
# Powered By   : Artist
# Type         : API Based Telegram Music Bot
#
# Bot          : @ArtistApibot
# Channel      : https://t.me/artistbots
# GitHub       : https://github.com/elevenyts
#
# Unauthorized copying, modification, or redistribution
# of this source code without permission is prohibited.
# ==========================================================

from pyrogram import enums, errors, filters, types

from Elevenyts import app, config, db, lang
from Elevenyts.helpers import buttons, utils

CUSTOM_EMOJI_IDS = {
    "🌟": "5206285830666076912",
    "😎": "6100624791947977185",
    "🎀": "5242311354919963946",
    "🤩": "6118538967395605278",
}

def make_custom_emoji_entities(text):
    entities = []
    for emoji, emoji_id in CUSTOM_EMOJI_IDS.items():
        start = 0
        while True:
            index = text.find(emoji, start)
            if index == -1:
                break
            offset = len(text[:index].encode("utf-16-le")) // 2
            length = len(emoji.encode("utf-16-le")) // 2
            entities.append(types.MessageEntity(
                type=enums.MessageEntityType.CUSTOM_EMOJI,
                offset=offset,
                length=length,
                custom_emoji_id=emoji_id,
            ))
            start = index + len(emoji)
    return sorted(entities, key=lambda entity: entity.offset)



@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    """Handle /help command in private chats - shows help menu with image."""
    # Auto-delete command message
    try:
        await m.delete()
    except Exception:
        pass
    
    try:
        await m.reply_photo(
            photo=config.START_IMG,  # Use same image as start command
            caption=m.lang["help_menu"],
            reply_markup=buttons.help_markup(m.lang),
            quote=True,
        )
    except Exception:
        # Fallback to text if photo fails
        await m.reply_text(
            text=m.lang["help_menu"],
            reply_markup=buttons.help_markup(m.lang),
            quote=True,
        )


@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    """
    Handle /start command - welcome message for users.

    - In private chat: Shows welcome message with inline buttons
    - In group chat: Shows short welcome message
    - Adds new users to database
    - Sends log to logger group for new users
    """
    # Auto-delete command message in group chats
    if message.chat.type != enums.ChatType.PRIVATE:
        try:
            await message.delete()
        except Exception:
            pass
    
    # Skip if message from channel or anonymous admin
    if not message.from_user:
        return

    # Check if user is blacklisted
    if message.from_user.id in app.bl_users and message.from_user.id not in db.notified:
        return await message.reply_text(message.lang["bl_user_notify"])

    # If /start help, show help menu
    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    # Determine if chat is private or group
    private = message.chat.type == enums.ChatType.PRIVATE

    # Choose appropriate welcome message
    _text = (
        message.lang["start_pm"].format(message.from_user.first_name, app.name)
        if private
        else message.lang["start_gp"].format(app.name)
    )

    key = buttons.start_key(message.lang, private)
    if private:
        _text = _text.replace("🕊️", "😎").replace("✨", "🤩")
    entities = make_custom_emoji_entities(_text) if private else []
    media = await db.cache.find_one({"_id": "start_welcome_media"}) if private else None
    try:
        if private and media and media.get("type") == "video":
            await message.reply_video(
                video=media["file_id"],
                caption=_text,
                caption_entities=entities,
                reply_markup=key,
            )
        else:
            photo = media.get("file_id") if private and media and media.get("type") == "photo" else config.START_IMG
            await message.reply_photo(
                photo=photo,
                caption=_text,
                caption_entities=entities,
                reply_markup=key,
            )
    except Exception as e:
        print(f"Start media error: {e}")
        await message.reply_text(
            text=_text,
            entities=entities,
            reply_markup=key,
            quote=not private,
        )

    # For private chats, add user to database if new
    if private:
        if await db.is_user(message.from_user.id):
            return  # User already exists, no need to add
        # Log new user to logger group
        await utils.send_log(message)
        # Add user to database
        return await db.add_user(message.from_user.id)


@app.on_message(filters.command(["playmode", "settings"]) & filters.group & ~app.bl_users)
@lang.language()
async def settings(_, message: types.Message):
    """
    Handle /playmode or /settings command - show group settings.

    Displays:
    - Play mode (everyone or admin only)
    - Current language
    - Options to change settings
    """
    # Auto-delete command message
    try:
        await message.delete()
    except Exception:
        pass
    
    admin_only = await db.get_play_mode(message.chat.id)  # Get play mode setting
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
    """
    Handle new member events - detect when bot is added to groups.

    - Leaves non-supergroup chats
    - Adds new groups to database
    """
    # Only work in supergroups (not basic groups)
    if message.chat.type != enums.ChatType.SUPERGROUP:
        return await message.chat.leave()

    # Check each new member
    for member in message.new_chat_members:
        if member.id == app.id:  # Bot itself was added
            if await db.is_chat(message.chat.id):
                return  # Chat already in database
            # Add chat to database (log is sent from new_chat.py with photo)
            await db.add_chat(message.chat.id)
            
