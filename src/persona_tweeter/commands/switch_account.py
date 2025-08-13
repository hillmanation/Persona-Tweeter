from discord import app_commands, Interaction
def register(bot):
    @bot.tree.command(description="Set your default account key (stub).")
    async def switch_account(interaction: Interaction, account: str):
        await interaction.response.send_message(f"Default account set to **{account}** (stub).", ephemeral=True)
