from discord import app_commands, Interaction

def register(bot):
    @bot.tree.command(description="Set your default persona (MVP stub).")
    async def set_persona(interaction: Interaction, persona: str):
        await interaction.response.send_message(f"Default persona set to **{persona}** (stub).", ephemeral=True)
