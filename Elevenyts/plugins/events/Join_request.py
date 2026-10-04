# ==========================================================
# Join Request Verify Handler
# ==========================================================

from pyrogram.types import (
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Elevenyts import app


@app.on_chat_join_request()
async def handle_join_request(client, request: ChatJoinRequest):

    user = request.from_user

    if not user:
        return

    # Group name automatically
    group_name = request.chat.title or "this group"

    # RnxMusic2Bot start link
    deep_link = "https://t.me/Rnxmusic2_bot?start=verify"

    # Verify button
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "「 ✓ ᴠᴇʀɪғʏ ɴᴏᴡ 」",
                    url=deep_link
                )
            ]
        ]
    )

    # Message
    text = (
        "╭─━━━━━━━━━━━━━━━━━━━━─╮\n"
        "        ʀɴ x ᴍᴜsɪᴄ 🕊\n"
        "╰─━━━━━━━━━━━━━━━━━━━━─╯\n\n"
        "        ᴀᴄᴄᴇss ʀᴇǫᴜᴇsᴛᴇᴅ\n\n"
        "ʏᴏᴜ'ᴠᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴀᴄᴄᴇss ᴛᴏ\n"
        f"<b>{group_name}</b>\n\n"
        "ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴀɪᴛɪɴɢ ғᴏʀ\n"
        "ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ. ᴄᴏᴍᴘʟᴇᴛᴇ ᴛʜᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ\n"
        "ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ʏᴏᴜʀ ᴇɴᴛʀʏ.\n\n"
        "╭─━━━━━━━━━━━━━━━━━━━━─╮\n"
        "   🔐 ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ\n"
        "╰─━━━━━━━━━━━━━━━━━━━━─╯\n\n"
        "✦ sᴀғᴇ • ғᴀsᴛ • ᴏɴᴇ ᴛᴀᴘ"
    )

    try:
        await client.send_message(
            chat_id=user.id,
            text=text,
            reply_markup=markup
        )

        print(f"✅ Verify message sent to {user.id}")

    except Exception as e:
        print(f"❌ Join Request DM Error: {e}")
