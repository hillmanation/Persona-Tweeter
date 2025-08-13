# Project Plan — Ray Zee Discord Bot + Twitter Integration

## **Project Goals**
1. **Propose→Approve→Post flow**: Users call a slash command, the bot drafts a tweet in “Ray Zee” voice (via system prompt), shows it for approval/reroll, then posts to the **Ray Zee** account via the X API once approved.
2. **Reply to an existing tweet**: User supplies a tweet URL → bot fetches tweet text + media → sends text + image description (via ChatGPT vision) into the Ray-Zee prompt → generates a reply → user approves/rerolls → bot posts reply.
3. **Caption an image**: User uploads an image → bot analyzes it (vision) → drafts a Ray-Zee caption → approve/reroll → post with media.
4. **Multi-account, multi-persona**: Easily swap which X account to post as and which persona prompt to use, via config and/or slash commands.

---

## **Key Slash Commands (MVP)**
- `/link_twitter` – OAuth link flow for the account owner (once per X account).
- `/propose_tweet prompt:"…" [persona] [account]` – Draft a tweet from a user idea.
- `/reroll` – Rerun the last proposal with same inputs.
- `/approve` – Post the last approved draft to the selected account.
- `/reply_to_tweet url:"…" [persona] [account]` – Pull tweet text/media → draft Ray-Zee reply.
- `/caption_image [persona] [account]` (with attachment) – Analyze image → draft caption → approve→post.
- `/switch_account account:"…"` – Set default target account for the guild/channel/user.
- `/set_persona persona:"…"` – Set default persona (e.g., “RayZee”, “OtherParody”).
- `/unlink_twitter` – Revoke the stored tokens for current user/account.

---

## **Architecture Overview**
**Discord Layer (discord.py)**
- Slash commands, ephemeral previews, button components for **Approve / Reroll / Cancel**.
- Short-lived “proposal session” state per user/channel (cache + DB).

**Auth & Accounts**
- **OAuth 2.0 + PKCE** to link X accounts (read+write; add `media.write` when needed).
- Store per-account tokens (access/refresh/expiry) with safe rotation.

**Generators (OpenAI)**
- Text generation (Chat Completions) with **persona system prompts**.
- Vision: send image URL/file to the model to extract a description or scene tags that feed the Ray-Zee prompt.

**Twitter (X API v2)**
- **Create Tweet**: `POST /2/tweets` (text), or text+`media_ids`.
- **Reply**: same endpoint with `reply.in_reply_to_tweet_id`.
- **Media Upload**: `/2/media/upload` → returns `media_id` → include in tweet.
- **Fetch source tweet**: `GET /2/tweets?ids=…&expansions=attachments.media_keys&media.fields=url,alt_text,preview_image_url` → get text + media URLs.

**Storage**
- SQLite (MVP) or Postgres (prod):
  - `accounts`: {account_key, screen_name, twitter_user_id, access_token, refresh_token, expires_at}
  - `personas`: {name, system_prompt, safety/sanitization rules}
  - `defaults`: {scope: guild/channel/user, default_account, default_persona}
  - `proposals`: {id, requester, persona, account_key, input_prompt, draft_text, media_refs, expires_at, status}

**Config**
- YAML/JSON for **accounts** and **personas**; DB overrides via slash commands.
- Allows quick swap to other parody users without code changes.

---

## **Core Flows**

### A) Propose → Approve → Post
1. `/propose_tweet "topic"` (optional `persona`, `account`)
2. Bot builds **messages**:
   - `system`: Ray-Zee (from persona store)
   - `user`: brief task with constraints (char limit, hashtags, tone)
3. Show ephemeral **Preview** with buttons: Approve / Reroll / Cancel.
4. On **Approve**:
   - Ensure fresh access token (refresh if needed)
   - `POST /2/tweets` (or include `media_ids` later)
   - Return link to posted tweet.

### B) Reply to Tweet URL
1. `/reply_to_tweet url`
2. Parse tweet ID → **GET /2/tweets…** with expansions
3. If media present, send each image URL to **vision** to get descriptions/tags
4. Compose a **reply prompt** (source text + vision tags) under the Ray-Zee system prompt
5. Preview → Approve → `POST /2/tweets` with `reply.in_reply_to_tweet_id=<id>`.

### C) Caption Image
1. `/caption_image` with image attachment
2. Send image to **vision** → get objects/scene/mood
3. Prompt Ray-Zee to generate a **caption** (and optional hashtags) within limits
4. **Upload media** to X → collect `media_id`
5. Preview → Approve → `POST /2/tweets` with `media_ids`.

---

## **Prompting Methodology (Persona-First, Param-Aware)**
- **Fixed System Prompt**: your “Ray Zee” block (kept immutable).
- **Instruction Layer** (assistant or system): hard rules (max ~240 chars to leave hashtag room, avoid slurs, no doxxing, etc.).
- **User Layer**: topic or seed idea.
- **Tool Hints**: include any constraints (hashtags, mention handling, reply context, media description).
- **Reroll**: re-call with same system + updated seed (“more bite”, “shorter”, “+1 emoji”, etc.).
- **Guardrails**: add a policy check step.

---

## **Rate Limits & Resilience**
- Maintain **per-app and per-account** counters (24h windows).
- Backoff on 429 using `x-rate-limit-reset`.
- Log `x-rate-limit-remaining` for observability.
- Optional queue for retries.

---

## **Security & Safety**
- Encrypt tokens at rest.
- Scope tokens to **tweet.read / tweet.write / users.read / offline.access (+ media.write)**.
- Optional **content policy pass** before posting.
- Provide `/unlink_twitter`.

---

## **Minimal Data Structures (example)**
```yaml
# personas.yaml
personas:
  RayZee:
    system_prompt: |
      ... (your Ray Zee system prompt) ...
    max_chars: 240
    default_hashtags: ["#AmenGobbles"]

# accounts.yaml
accounts:
  rayzee:
    twitter_user_id: "1234567890"
    screen_name: "RayZeeOfficial"
    # tokens live in DB; this key maps to that record
```
---

## **Milestones**
**M1 — Foundations (Auth & Post)**
- OAuth 2.0 (PKCE) flow + token storage/refresh
- `/link_twitter`, `/propose_tweet`, `/approve`, `/reroll` (text-only post)
- Basic rate-limit handling and logging

**M2 — Replies**
- Tweet fetch + expansions
- Vision on media → enrich prompt
- `/reply_to_tweet` full approve→post flow

**M3 — Media & Captions**
- `/caption_image` with media upload
- Add `media.write` scope & `/2/media/upload`
- Character budgeting (text + media)

**M4 — Multi-Account / Multi-Persona**
- `/switch_account`, `/set_persona` + defaults per guild/channel/user
- Config+DB hybrid for easy swaps

**M5 — Hardening**
- Token encryption, audit logs, better error UX, retry queues, tests

---

## **Acceptance Criteria (MVP)**
- User can link the **Ray Zee** account once and keep it linked.
- `/propose_tweet` returns a Ray-Zee-style draft under 280 chars, consistently in-persona.
- **Approve** posts to the correct account; bot returns the X status URL.
- `/reply_to_tweet` reads a tweet (and image), generates an in-persona reply, and posts it on approval.
- `/caption_image` generates a caption and posts w/ media.
- `/switch_account` & `/set_persona` change defaults without restarts.
