import discord
from discord.ext import commands
from .storage import init_db
from .commands import (
    link_twitter, propose_tweet, approve, reroll,
    reply_to_tweet, caption_image, switch_account, set_persona, unlink_twitter
)

def create_bot():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        init_db()
        try:
            await bot.tree.sync()
        except Exception as e:
            print("Slash sync error:", e)
        print(f"Logged in as {bot.user}")

    # Register commands
    link_twitter.register(bot)
    propose_tweet.register(bot)
    approve.register(bot)
    reroll.register(bot)
    reply_to_tweet.register(bot)
    caption_image.register(bot)
    switch_account.register(bot)
    set_persona.register(bot)
    unlink_twitter.register(bot)

    return bot
