from discord import app_commands, Interaction
from typing import Optional
from ..config import PERSONAS
from ..openai_client import draft_tweet

# In-memory session store for simplicity (MVP)
SESSIONS = {}  # discord_id -> {'persona': str, 'account': str, 'draft': str, 'input': str}

def register(bot):
    @bot.tree.command(description="Draft a Ray-Zee style tweet.")
    @app_commands.describe(prompt="What should the tweet be about?", persona="Persona key (default RayZee)", account="Account key (default rayzee)")
    async def propose_tweet(interaction: Interaction, prompt: str, persona: Optional[str] = None, account: str = "rayzee"):
        await interaction.response.defer(ephemeral=True)
        persona = persona or "RayZee"
        p = PERSONAS.get(persona)
        if not p:
            await interaction.followup.send(f"Unknown persona '{persona}'.", ephemeral=True)
            return
        system = p["system_prompt"]
        max_chars = int(p.get("max_chars", 240))
        user_prompt = f"Draft a single X (Twitter) post under {max_chars} characters. Topic: {prompt}"
        try:
            text = draft_tweet(system, user_prompt)
        except Exception as e:
            await interaction.followup.send(f"Generation error: {e}", ephemeral=True)
            return
        SESSIONS[interaction.user.id] = {"persona": persona, "account": account, "draft": text, "input": prompt}
        await interaction.followup.send(f"**Draft:**
{text}

Use `/approve` to post or `/reroll` to try again.", ephemeral=True)
