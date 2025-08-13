from discord import app_commands, Interaction

def register(bot):
    @bot.tree.command(description="Link your X (Twitter) account (OAuth 2.0 PKCE).")
    async def link_twitter(interaction: Interaction, account: str = "rayzee"):
        link = f"http://{interaction.client.user}"
        # We don't know the bot's public URL; build local helper link:
        link = f"http://{__import__('rayzee_bot.config').rayzee_bot.config.OAUTH_SERVER_HOST}:{__import__('rayzee_bot.config').rayzee_bot.config.OAUTH_SERVER_PORT}/start?discord_id={interaction.user.id}&account_key={account}"
        await interaction.response.send_message(f"Click to link your X account for **{account}**:
{link}", ephemeral=True)
