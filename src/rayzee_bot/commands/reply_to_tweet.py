from discord import app_commands, Interaction
from typing import Optional
from ..storage import get_tokens
from ..twitter_api import fetch_tweet_with_media, post_tweet
from ..openai_client import draft_tweet, describe_image_stub
from ..config import PERSONAS

def register(bot):
    @bot.tree.command(description="Draft a Ray-Zee style reply to a tweet URL.")
    @app_commands.describe(url="Tweet URL", persona="Persona key (default RayZee)", account="Account key (default rayzee)")
    async def reply_to_tweet(interaction: Interaction, url: str, persona: Optional[str] = None, account: str = "rayzee"):
        await interaction.response.defer(ephemeral=True)
        persona = persona or "RayZee"
        p = PERSONAS.get(persona)
        if not p:
            await interaction.followup.send(f"Unknown persona '{persona}'.", ephemeral=True)
            return
        tokens = get_tokens(interaction.user.id, account)
        if not tokens:
            await interaction.followup.send(f"Not linked for account '{account}'. Use `/link_twitter`.", ephemeral=True)
            return
        # naive tweet id parse
        tid = url.rstrip('/').split('/')[-1].split('?')[0]
        try:
            src = fetch_tweet_with_media(tokens['access_token'], tid)
        except Exception as e:
            await interaction.followup.send(f"Fetch error: {e}", ephemeral=True)
            return

        text = ""
        media_desc = ""
        if src.get("data"):
            text = src["data"][0].get("text","")
        includes = src.get("includes",{})
        media = includes.get("media",[])
        if media:
            # describe first image only (stub)
            m = media[0]
            if m.get("url"):
                media_desc = describe_image_stub(m["url"])

        prompt = f"Reply in persona. Original tweet text: '{text}'. Image notes: '{media_desc}'. Keep under {int(p.get('max_chars',240))} chars."
        try:
            draft = draft_tweet(p['system_prompt'], prompt)
        except Exception as e:
            await interaction.followup.send(f"Generation error: {e}", ephemeral=True)
            return
        await interaction.followup.send(f"**Draft reply to {tid}:**
{draft}

(Use `/approve` after `/propose_tweet` flow; reply posting wiring TODO.)", ephemeral=True)
