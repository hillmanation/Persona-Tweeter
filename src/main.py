import os
from dotenv import load_dotenv
load_dotenv()

from persona_tweeter.ui import create_bot
from persona_tweeter.oauth_server import start_oauth_server

def main():
    start_oauth_server()
    bot = create_bot()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    main()
