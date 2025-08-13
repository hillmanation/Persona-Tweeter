import base64, hashlib, secrets, time, threading
from urllib.parse import urlencode, quote_plus
import requests
from flask import Flask, request, redirect, Response
from .config import X_CLIENT_ID, X_CLIENT_SECRET, X_REDIRECT_URI, OAUTH_SERVER_HOST, OAUTH_SERVER_PORT
from .storage import save_tokens
from .twitter_api import exchange_code_for_tokens, get_user_me

app = Flask(__name__)

AUTH_STATE = {}  # state -> {discord_id, account_key, code_verifier, ts}

def _b64url(b: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")

def _gen_pkce_pair():
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode('ascii')).digest())
    return verifier, challenge

@app.get("/start")
def start():
    discord_id = request.args.get("discord_id")
    account_key = request.args.get("account_key", "rayzee")
    if not discord_id:
        return Response("missing discord_id", 400)
    verifier, challenge = _gen_pkce_pair()
    state = _b64url(secrets.token_bytes(24))
    AUTH_STATE[state] = {"discord_id": discord_id, "account_key": account_key, "code_verifier": verifier, "ts": time.time()}
    params = {
        "response_type": "code",
        "client_id": X_CLIENT_ID,
        "redirect_uri": X_REDIRECT_URI,
        "scope": "tweet.read tweet.write users.read offline.access",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return redirect("https://twitter.com/i/oauth2/authorize?" + urlencode(params, quote_via=quote_plus))

@app.get("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    if not code or not state or state not in AUTH_STATE:
        return Response("invalid state or code", 400)
    rec = AUTH_STATE.pop(state)
    tok = exchange_code_for_tokens(
        X_CLIENT_ID, code, rec["code_verifier"], X_REDIRECT_URI, X_CLIENT_SECRET
    )
    access_token = tok["access_token"]
    refresh_token = tok.get("refresh_token")
    expires_in = tok.get("expires_in", 3600)
    user = get_user_me(access_token)
    save_tokens(rec["discord_id"], rec["account_key"], user.get("id"), user.get("username"), access_token, refresh_token, expires_in)
    return Response(f"Linked @{user.get('username')} to account '{rec['account_key']}'. You can close this tab.", 200)

def start_oauth_server():
    t = threading.Thread(target=lambda: app.run(host=OAUTH_SERVER_HOST, port=OAUTH_SERVER_PORT, debug=False, use_reloader=False), daemon=True)
    t.start()
