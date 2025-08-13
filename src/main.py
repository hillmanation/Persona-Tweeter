import os
from dotenv import load_dotenv
load_dotenv()

from rayzee_bot.ui import create_bot
from rayzee_bot.oauth_server import start_oauth_server

def main():
    # Start the OAuth helper server in a background thread
    start_oauth_server()
    # Start discord bot (slash commands are registered on_ready)
    bot = create_bot()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    main()
