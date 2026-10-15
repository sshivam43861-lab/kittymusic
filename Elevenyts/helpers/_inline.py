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
from pyrogram import types
from pyrogram.enums import ButtonStyle
from Elevenyts import app, config, lang


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [[
                self.ikb(
                    text=text,
                    callback_data="cancel_dl",
                    style=ButtonStyle.PRIMARY,
                )
            ]]
        )

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []

        if status:
            keyboard.append(
                [
                    self.ikb(
                        text=status,
                        callback_data=f"controls status {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    )
                ]
            )
        elif timer:
            keyboard.append(
                [
                    self.ikb(
                        text=timer,
                        callback_data=f"controls status {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    )
                ]
            )

        if not remove:
            # Autoplay button row
            keyboard.append(
                [
                    self.ikb(
                        text="♫ 𝐀‌υᴛσᴘℓᴀʏ ♫",
                        callback_data=f"autoplay_toggle {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    )
                ]
            )

            # Main control buttons row
            keyboard.append(
                [
                    self.ikb(
                        text="♫ 𝐑‌єѕυᴍє ♫",
                        callback_data=f"controls resume {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="♫ 𝐏‌ᴀυѕє ♫",
                        callback_data=f"controls pause {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="♫ 𝐑‌єᴘℓᴀʏ ♫",
                        callback_data=f"controls replay {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="♫ 𝐒‌κɪᴘ ♫",
                        callback_data=f"controls skip {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="♫ 𝐒‌ᴛσᴘ ♫",
                        callback_data=f"controls stop {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(
        self, _lang: dict, back: bool = False
    ) -> types.InlineKeyboardMarkup:
        """Create help menu with categorized buttons."""

        if back:
            rows = [
                [
                    self.ikb(
                        text="♫ 𝐁‌ᴀᴄκ ♫",
                        callback_data="help_main",
                        style=ButtonStyle.PRIMARY,
                    ),
                ]
            ]
        else:
            # Help menu with categorized buttons (3 per row)
            rows = [
                [
                    self.ikb(
                        text="𝐀‌ᴅᴍɪɴꜱ",
                        callback_data="help_admins",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐀‌υᴛʜ",
                        callback_data="help_auth",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐁‌ʀσᴀᴅᴄᴀꜱᴛ",
                        callback_data="help_broadcast",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐁‌ℓ-ᴄʜᴀᴛ",
                        callback_data="help_blchat",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐁‌ℓ-υѕєʀ",
                        callback_data="help_bluser",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐆‌-𝐁‌ᴀη",
                        callback_data="help_gban",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐋‌σσᴘ",
                        callback_data="help_loop",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐏‌ℓᴀʏ",
                        callback_data="help_play",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐐‌υєυє",
                        callback_data="help_queue",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐒‌єєκ",
                        callback_data="help_seek",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐒‌ʜυꜰꜰℓє",
                        callback_data="help_shuffle",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐏‌ɪɴɢ",
                        callback_data="help_ping",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐒‌ᴛᴀᴛѕ",
                        callback_data="help_stats",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐒‌υᴅσ",
                        callback_data="help_sudo",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐌‌ᴀɪɴᴛєɴᴀɴᴄє",
                        callback_data="help_maintenance",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐓‌ᴀɢ 𝐀‌ℓℓ",
                        callback_data="tagall_info",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="♫ 𝐁‌ᴀᴄκ ♫",
                        callback_data="start",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
            ]

        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="𝐂‌ʜᴀɴɴєℓ",
                        url=config.SUPPORT_CHANNEL,
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐒‌υᴘᴘσʀᴛ",
                        url=config.SUPPORT_CHAT,
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐀‌ᴅᴅ 𝐓‌σ 𝐆‌ʀσυᴘ",
                        url=f"https://t.me/{app.username}?startgroup=true",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
            ]
        )

    def play_queued(
    self, chat_id: int, item_id: str, _text: str
) -> types.InlineKeyboardMarkup:
    return self.ikm(
        [[
            self.ikb(
                text="▷ 𝐏‌ℓᴀʏ 𝐍‌σω",
                callback_data=f"controls force {chat_id} {item_id}",
                style=ButtonStyle.PRIMARY,
            )
        ]]
    )

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"

        return self.ikm(
            [
                [
                    self.ikb(
                        text=_text,
                        callback_data=f"controls {_action} {chat_id} q",
                        style=ButtonStyle.PRIMARY,
                    )
                ]
            ]
        )

    def settings_markup(
        self, lang: dict, admin_only: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=lang["play_mode"] + " ➜",
                        callback_data=f"controls status {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text=admin_only,
                        callback_data="playmode",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
            ]
        )

    def start_key(
        self, lang: dict, private: bool = False
    ) -> types.InlineKeyboardMarkup:
        rows = [
            [
                self.ikb(
                    text="𝐀‌ᴅᴅ 𝐓‌σ 𝐆‌ʀσυᴘ",
                    url=f"https://t.me/{app.username}?startgroup=true",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
            [
                self.ikb(
                    text="🪄 𝐃‌єᴠ",
                    url="https://t.me/Deadlock93",
                    style=ButtonStyle.PRIMARY,
                ),
                self.ikb(
                    text="🦋 𝐒‌υᴘᴘσʀᴛ",
                    url="https://t.me/RnMusicUpdates",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
            [
                self.ikb(
                    text="🌙 𝐔‌ᴘᴅᴀᴛєѕ",
                    url="https://t.me/RnMusicUpdates",
                    style=ButtonStyle.PRIMARY,
                ),
                self.ikb(
                    text="♫ 𝐇‌єℓᴘ & 𝐂‌σᴍᴍᴀηᴅ 𝐆‌υɪᴅᴇ ♫",
                    callback_data="help",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
        ]

        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="𝐂‌σᴘʏ 𝐋‌ɪɴκ",
                        copy_text=link,
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text="𝐎‌ᴘєɴ 𝐈‌ɴ 𝐘‌συᴛυʙє",
                        url=link,
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
            ]
        )
