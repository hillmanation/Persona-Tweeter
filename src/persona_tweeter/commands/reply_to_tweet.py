from discord import app_commands, Interaction
from typing import Optional
from ..storage import get_tokens
from ..twitter_api import fetch_tweet_with_media
from ..openai_client import draft_tweet
from ..config import PERSONAS
from .propose_tweet import SESSIONS
import re

TWEET_URL_RE = re.compile(r'''
    ^https?://
    (?:twitter\.com|x\.com)/
    [^/]+/status/
    (?P<id>\d+)
''', re.IGNORECASE | re.VERBOSE)

def extract_tweet_id(url: str):
    m = TWEET_URL_RE.search(url.strip())
    if m:
        return m.group('id')
    tail = url.rstrip('/').split('/')[-1].split('?')[0]
    return tail if tail.isdigit() else None

def register(bot):
    @bot.tree.command(description="Draft a persona-style reply to a tweet URL (basic).")
    @app_commands.describe(url="Tweet URL", persona="Persona key (default BoomerParody)", account="Account key (default primary)")
    async def reply_to_tweet(interaction: Interaction, url: str, persona: Optional[str] = None, account: str = "primary"):
        await interaction.response.defer(ephemeral=True)
        persona = persona or "BoomerParody"
        p = PERSONAS.get(persona)
        if not p:
            await interaction.followup.send(f"Unknown persona '{persona}'.", ephemeral=True)
            return

        tid = extract_tweet_id(url)
        if not tid:
            await interaction.followup.send("Couldn't parse tweet ID from that URL. Please paste the full tweet URL.", ephemeral=True)
            return

        tokens = get_tokens(interaction.user.id, account)
        if not tokens:
            await interaction.followup.send(f"Not linked for account '{account}'. Use `/link_twitter`.", ephemeral=True)
            return

        try:
            src = fetch_tweet_with_media(tokens['access_token'], tid)
        except Exception as e:
            await interaction.followup.send(f"Fetch error: {e}", ephemeral=True)
            return

        src_text = ""
        if src.get("data"):
            item = src['data'][0]
            src_text = item.get('text', '')

        max_chars = int(p.get('max_chars', 240))
        system = p['system_prompt']
        user_prompt = (
            f"Reply in persona to the tweet below, under {max_chars} characters. "
            f"Do not quote the text verbatim; craft a fresh reply. "
            f"Source tweet text: {src_text!r}"
        )

        try:
            draft = draft_tweet(system, user_prompt)
        except Exception as e:
            await interaction.followup.send(f"Generation error: {e}", ephemeral=True)
            return

        SESSIONS[interaction.user.id] = {
            'persona': persona,
            'account': account,
            'draft': draft,
            'input': f"reply to {tid}",
            'in_reply_to': tid,
        }

        await interaction.followup.send(
            f"**Draft reply to {tid}:**\n{draft}\n\nUse `/approve` to post, or `/reroll` to try again.",
            ephemeral=True
        )
