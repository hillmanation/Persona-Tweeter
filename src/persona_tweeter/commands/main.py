import discord
from discord.ext import commands
from .commands import link_twitter, propose_tweet, approve, reroll, reply_to_tweet, caption_image

class PersonaTweeter(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        link_twitter.register(self)
        propose_tweet.register(self)
        approve.register(self)
        reroll.register(self)
        reply_to_tweet.register(self)
        caption_image.register(self)

def run_bot():
    import os
    token = os.getenv("DISCORD_TOKEN")
    bot = PersonaTweeter()
    bot.run(token)

if __name__ == "__main__":
    run_bot()
