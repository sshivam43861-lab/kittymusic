import asyncio
import json
import logging
import time
from pathlib import Path

from pyrogram import enums, errors

from Elevenyts import app

log = logging.getLogger(__name__)
DATA_FILE = Path(__file__).resolve().parents[2] / "non_admin_groups.json"
INTERVAL = 8 * 60 * 60
ADMIN_STATUSES = (
    enums.ChatMemberStatus.ADMINISTRATOR,
    enums.ChatMemberStatus.OWNER,
)

REMINDER = (
    "୨୧・🌸 ʜᴇʟʟᴏᴏ ᴀᴅᴍɪɴs! 🥺🎀\n\n"
    "ᴍᴇʀᴀ ᴀᴅᴍɪɴ ʙᴀɴɴᴇ ᴋᴀ ᴅʀᴇᴀᴍ ᴀʙʜɪ ʙʜɪ ᴘᴇɴᴅɪɴɢ ʜᴀɪ… 🐻💗\n"
    "ᴘʟᴇᴀsᴇ ᴍᴜᴊʜᴇ ᴀᴅᴍɪɴ ʙᴀɴᴀ ᴅᴏ ɴᴀ! 🎧🌷\n"
    "ᴘʜɪʀ ʜᴜᴍ sᴀᴀᴛʜ ᴍᴇɪɴ ᴍᴜsɪᴄ sᴜɴᴇɴɢᴇ! 🫶🏻🎶"
)


def _read():
    try:
        data = json.loads(DATA_FILE.read_text())
        if not isinstance(data, dict):
            return {}
        return {str(chat_id): float(ts) for chat_id, ts in data.items()}
    except (OSError, ValueError, TypeError):
        return {}


def _write(groups):
    temp = DATA_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(groups))
    temp.replace(DATA_FILE)


def track_group(chat_id):
    groups = _read()
    groups.setdefault(str(chat_id), time.time())
    _write(groups)


def forget_group(chat_id):
    groups = _read()
    if groups.pop(str(chat_id), None) is not None:
        _write(groups)


async def reminder_loop():
    await asyncio.sleep(30)

    while True:
        groups = _read()
        wall_now = time.time()

        for raw_chat_id, last_sent in list(groups.items()):
            try:
                chat_id = int(raw_chat_id)
                member = await app.get_chat_member(chat_id, app.id)

                if member.status in ADMIN_STATUSES:
                    groups.pop(raw_chat_id, None)
                    continue

                if wall_now - float(last_sent) >= INTERVAL:
                    await app.send_message(chat_id, REMINDER)
                    groups[raw_chat_id] = wall_now

            except errors.UserNotParticipant:
                groups.pop(raw_chat_id, None)
            except errors.ChatAdminRequired:
                log.debug("Cannot check bot status in %s yet", chat_id)
            except errors.ChannelPrivate:
                groups.pop(raw_chat_id, None)
            except errors.ChatWriteForbidden:
                log.warning(
                    "Cannot send admin reminder in %s: text sending is forbidden.",
                    chat_id,
                )
            except errors.FloodWait as exc:
                log.warning("Reminder flood wait: sleeping %s seconds", exc.value)
                await asyncio.sleep(exc.value)
            except Exception as exc:
                log.warning("Admin reminder failed in %s: %s", raw_chat_id, exc)

        _write(groups)
        await asyncio.sleep(60)
