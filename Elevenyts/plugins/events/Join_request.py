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

    # RnxMusic2Bot start link
    deep_link = "https://t.me/Rnxmusic2_bot?start=verify"

    # Verify button
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Verify",
                    url=deep_link
                )
            ]
        ]
    )

    try:
        await client.send_message(
            chat_id=user.id,
            text=(
                "<b>👋 Welcome!</b>\n\n"
                "You have requested to join the group.\n\n"
                "Click the button below to verify yourself."
            ),
            reply_markup=markup
        )

        print(f"✅ Verify message sent to user: {user.id}")

    except Exception as e:
        print(f"❌ Join Request DM Error: {e}")
