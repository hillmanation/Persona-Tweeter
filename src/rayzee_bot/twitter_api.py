import time, requests
from typing import Optional, List
from .config import X_CLIENT_ID, X_CLIENT_SECRET, X_REDIRECT_URI
from .config import OAUTH_SERVER_HOST, OAUTH_SERVER_PORT
from .storage import save_tokens
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
USER_ME_URL = "https://api.twitter.com/2/users/me"
TWEETS_URL = "https://api.twitter.com/2/tweets"
MEDIA_UPLOAD_URL = "https://api.twitter.com/2/media/upload"
TWEETS_FETCH_URL = "https://api.twitter.com/2/tweets"

def exchange_code_for_tokens(client_id, code, code_verifier, redirect_uri, client_secret=None):
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
        "code": code,
    }
    auth = None
    if client_secret:
        auth = (client_id, client_secret)
    r = requests.post(TOKEN_URL, data=data, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()

def refresh_access_token(client_id, refresh_token, client_secret=None):
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }
    auth = None
    if client_secret:
        auth = (client_id, client_secret)
    r = requests.post(TOKEN_URL, data=data, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()

def get_user_me(access_token):
    r = requests.get(USER_ME_URL, headers={"Authorization": f"Bearer {access_token}"}, timeout=15)
    r.raise_for_status()
    return r.json().get("data", {})

def post_tweet(access_token: str, text: str, in_reply_to: Optional[str]=None, media_ids: Optional[List[str]]=None):
    payload = {"text": text}
    if in_reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": in_reply_to}
    if media_ids:
        payload["media"] = {"media_ids": media_ids}
    r = requests.post(TWEETS_URL, headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }, json=payload, timeout=30)
    if r.status_code == 429:
        # Surface a useful message; real app could queue retry
        raise RuntimeError(f"Rate limited (429): {r.headers.get('x-rate-limit-reset')}")
    r.raise_for_status()
    return r.json()

def fetch_tweet_with_media(access_token: str, tweet_id: str):
    params = {
        "ids": tweet_id,
        "expansions": "attachments.media_keys",
        "media.fields": "url,alt_text,preview_image_url"
    }
    r = requests.get(TWEETS_FETCH_URL, headers={"Authorization": f"Bearer {access_token}"}, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

# TODO: implement v2 media upload if your tier supports it (media.write needed).
def upload_media_stub(access_token: str, filepath: str):
    raise NotImplementedError("Implement /2/media/upload here when ready.")
