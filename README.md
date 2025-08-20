# Persona Tweeter — Starter Repo

A modular **discord.py** bot that drafts persona-driven tweets using the OpenAI API and posts to X (Twitter) via the X API v2 as well as Bluesky. Includes OAuth 2.0 (PKCE) link flow, multi-account & multi-persona support, preview/approval, and stubs for replies and image captions.

## Quick start
1. Create a virtual env and install deps:
   ```bash
   python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill values.
3. Run the bot:
   ```bash
   python -m src.main
   ```

## Structure
```
persona-tweeter/
  config/
    personas.yaml
    accounts.yaml
  src/
    persona_tweeter/
      __init__.py
      config.py
      storage.py
      twitter_api.py
      openai_client.py
      oauth_server.py
      ui.py
      commands/
        __init__.py
        link_twitter.py
        propose_tweet.py
        approve.py
        reroll.py
        reply_to_tweet.py
        caption_image.py
        switch_account.py
        set_persona.py
        unlink_twitter.py
    main.py
  scripts/
    init_db.py
  tests/
    test_stub.py
  requirements.txt
  .env.example
  README.md
```

## Notes
- Media upload and vision/image captioning are stubbed with clear TODOs.
- Tokens are stored in SQLite (encrypt at rest for production).
- Scopes in the X developer portal: `tweet.read tweet.write users.read offline.access media.write`.
