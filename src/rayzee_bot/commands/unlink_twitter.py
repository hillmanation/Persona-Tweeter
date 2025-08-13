from discord import app_commands, Interaction

def register(bot):
    @bot.tree.command(description="Unlink your X account (MVP stub).")
    async def unlink_twitter(interaction: Interaction, account: str = "rayzee"):
        await interaction.response.send_message(f"Unlinked account **{account}** (stub; implement DB delete).", ephemeral=True)
