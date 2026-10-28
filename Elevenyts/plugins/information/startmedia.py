from pyrogram import filters, types
from Elevenyts import app, db

MEDIA_KEY = "start_welcome_media"


@app.on_message(filters.command("startmedia") & filters.private & filters.user(app.owner))
async def startmedia_status(_, message: types.Message):
    doc = await db.cache.find_one({"_id": MEDIA_KEY})
    if not doc:
        return await message.reply_text(
            "No custom start media saved yet.\n"
            "Reply to a photo with /setstartphoto or a video with /setstartvideo."
        )

    return await message.reply_text(
        f"Current saved media: <b>{doc.get('type', 'unknown')}</b>\n"
        "Use /setstartphoto or /setstartvideo by replying to the media you want."
    )


@app.on_message(filters.command("setstartphoto") & filters.private & filters.user(app.owner))
async def setstartphoto(_, message: types.Message):
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return await message.reply_text(
            "Reply to a photo with /setstartphoto."
        )

    await db.cache.update_one(
        {"_id": MEDIA_KEY},
        {"$set": {"type": "photo", "file_id": replied.photo.file_id}},
        upsert=True,
    )
    await message.reply_text("✅ Start photo saved.")


@app.on_message(filters.command("setstartvideo") & filters.private & filters.user(app.owner))
async def setstartvideo(_, message: types.Message):
    replied = message.reply_to_message
    if not replied or not replied.video:
        return await message.reply_text(
            "Reply to a video with /setstartvideo."
        )

    await db.cache.update_one(
        {"_id": MEDIA_KEY},
        {"$set": {"type": "video", "file_id": replied.video.file_id}},
        upsert=True,
    )
    await message.reply_text("✅ Start video saved.")

@app.on_message(filters.command("checkemoji") & filters.private & filters.user(app.owner))
async def checkemoji(_, message: types.Message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text(
            "Reply to the forwarded emoji message with /checkemoji."
        )

    entities = (replied.entities or []) + (replied.caption_entities or [])
    custom = [
        e for e in entities
        if e.type == types.MessageEntityType.CUSTOM_EMOJI
    ]

    if not custom:
        return await message.reply_text(
            "No custom emoji entities found in that message."
        )

    result = "\n".join(
        f"ID: {e.custom_emoji_id} | Offset: {e.offset} | Length: {e.length}"
        for e in custom
    )
    await message.reply_text(f"<b>Custom Emoji IDs:</b>\n<code>{result}</code>")
