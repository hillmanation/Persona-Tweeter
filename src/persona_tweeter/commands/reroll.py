from discord import app_commands, Interaction
from ..config import PERSONAS
from ..openai_client import draft_tweet
from .propose_tweet import SESSIONS

def register(bot):
    @bot.tree.command(description="Reroll the last proposal with same inputs.")
    async def reroll(interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        sess = SESSIONS.get(interaction.user.id)
        if not sess:
            await interaction.followup.send("No draft to reroll. Use `/propose_tweet` first.", ephemeral=True)
            return
        p = PERSONAS.get(sess['persona'])
        try:
            text = draft_tweet(p['system_prompt'], f"Draft a single X (Twitter) post under {int(p.get('max_chars',240))} chars. Topic: {sess['input']}")
            sess['draft'] = text
            await interaction.followup.send(f"**New draft:**\n{text}\n\nUse `/approve` to post.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Generation error: {e}", ephemeral=True)
