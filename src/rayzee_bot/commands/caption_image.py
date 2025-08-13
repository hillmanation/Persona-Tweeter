from discord import app_commands, Interaction
from typing import Optional
from ..config import PERSONAS

def register(bot):
    @bot.tree.command(description="Draft a Ray-Zee caption for an attached image (MVP stub).")
    async def caption_image(interaction: Interaction, persona: Optional[str] = None, account: str = "rayzee"):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Image captioning is stubbed. TODO: accept attachment, run vision, draft caption, upload media, and post.", ephemeral=True)
