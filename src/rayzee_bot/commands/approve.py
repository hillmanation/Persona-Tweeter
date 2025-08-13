from discord import app_commands, Interaction
from ..storage import get_tokens
from ..twitter_api import post_tweet
from .propose_tweet import SESSIONS

def register(bot):
    @bot.tree.command(description="Approve and post the last draft.")
    async def approve(interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        sess = SESSIONS.get(interaction.user.id)
        if not sess:
            await interaction.followup.send("No draft to approve. Use `/propose_tweet` first.", ephemeral=True)
            return
        tokens = get_tokens(interaction.user.id, sess['account'])
        if not tokens:
            await interaction.followup.send(f"Not linked for account '{sess['account']}'. Use `/link_twitter`.", ephemeral=True)
            return
        try:
            result = post_tweet(tokens['access_token'], sess['draft'])
            url = f"https://x.com/{tokens.get('screen_name')}/status/{result['data']['id']}"
            await interaction.followup.send(f"Posted: {url}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Post error: {e}", ephemeral=True)
