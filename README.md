# Ray Zee Bot — Starter Repo

A modular **discord.py** bot that drafts **Ray Zee**-style tweets using the ChatGPT API, previews them for approval, and posts to X (Twitter) via API v2. Includes OAuth 2.0 (PKCE) link flow, multi-account persona switching, and stubs for replies & image captions.

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
rayzee-starter/
  config/
    personas.yaml
    accounts.yaml
  src/
    rayzee_bot/
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
  rayzee_project_plan.md
```

## Notes
- Media upload and vision/image captioning are stubbed with clear TODOs.
- Tokens are stored in SQLite (encrypted-at-rest recommended for production).
- Adjust scopes in the X developer portal: `tweet.read tweet.write users.read offline.access media.write`.
