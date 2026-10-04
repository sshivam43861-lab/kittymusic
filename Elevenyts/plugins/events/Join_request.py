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

    # Get the actual group name
    group_name = request.chat.title or "this group"

    # RnxMusic2Bot verification link
    deep_link = "https://t.me/Rnxmusic2_bot?start=verify"

    # Inline Verify button
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ ᴠᴇʀɪғʏ ɴᴏᴡ",
                    url=deep_link
                )
            ]
        ]
    )

    # Verification message
    text = (
        "╭─━━━━━━━━━━━━━━─╮\n"
        "      ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ\n"
        "╰─━━━━━━━━━━━━━━─╯\n"
        f"ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ\n"
        f"<b>{group_name}</b> ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ.\n\n"
        "ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ\n"
        "ᴀɴᴅ ᴄᴏɴᴛɪɴᴜᴇ."
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
