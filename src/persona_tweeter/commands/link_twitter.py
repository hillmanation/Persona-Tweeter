from discord import app_commands, Interaction
from ..config import OAUTH_SERVER_HOST, OAUTH_SERVER_PORT

def register(bot):
    @bot.tree.command(description="Link your X (Twitter) account (OAuth 2.0 PKCE).")
    async def link_twitter(interaction: Interaction, account: str = "primary"):
        url = f"http://{OAUTH_SERVER_HOST}:{OAUTH_SERVER_PORT}/start?discord_id={interaction.user.id}&account_key={account}"
        await interaction.response.send_message(f"Click to link your X account for **{account}**:\n{url}", ephemeral=True)
