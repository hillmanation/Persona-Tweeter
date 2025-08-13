from discord import app_commands, Interaction
from typing import Optional

def register(bot):
    @bot.tree.command(description="Draft a persona-style caption for an image (stub).")
    async def caption_image(interaction: Interaction, persona: Optional[str] = None, account: str = "primary"):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Image captioning is stubbed. TODO: accept attachment, run vision, draft caption, upload media, and post.", ephemeral=True)
