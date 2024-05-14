from aiohttp import web
import plugins.web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="File Carry Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat("@falcon_sec")).invite_link
                if not link:
                    await self.export_chat_invite_link("@falcon_sec")
                    link = (await self.get_chat("@INDIAN_HACKER_GROUP")).invite_link
                self.invitelink = "t.me/falcon_sec"
            except Exception as a:
                self.LOGGER.warning(a)
                self.LOGGER.warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER.warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER.info("\nBot Stopped. Join https://t.me/ii_hacker_ii for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(-1002041085713)
            self.db_channel = -1002041085713
            test = await self.send_message(chat_id=CHANNEL_ID, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER.warning(e)
            self.LOGGER.warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER.info("\nBot Stopped. Join https://t.me/ii_hacker_ii for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info(f"Bot Running..!\n\nCreated by \nhttps://t.me/ii_Hacker_ii")
        self.LOGGER.info(f""" \n\n
_____ _____   
_  /    |  /   __/_   \__  | / /
  /_     /| |_  /  _  /    _  / / /_   |/ /
_  /   _  _ |  /_/ /_  / /_/ /_  /|  /
/_/      /_/  |_/_/\__/  \__/ /_/ |_/
                                SECURITY....
                                          """)
        self.username = usr_bot_me.username
        #web-response
        app = web.Application()
        app.add_routes([web.get('/', lambda request: web.Response(text="Hello, World!"))])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', PORT)
        await site.start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped.")

if __name__ == '__main__':
    bot = Bot()
    bot.run()
