import sqlite3, time
from .config import DB_PATH

SCHEMA = '''
CREATE TABLE IF NOT EXISTS user_tokens (
  discord_id TEXT NOT NULL,
  account_key TEXT NOT NULL,
  twitter_user_id TEXT,
  screen_name TEXT,
  access_token TEXT NOT NULL,
  refresh_token TEXT NOT NULL,
  expires_at INTEGER NOT NULL,
  PRIMARY KEY (discord_id, account_key)
);
CREATE TABLE IF NOT EXISTS defaults (
  scope TEXT NOT NULL,      -- 'guild:<id>' | 'channel:<id>' | 'user:<id>'
  key TEXT NOT NULL,        -- 'default_account' | 'default_persona'
  value TEXT NOT NULL,
  PRIMARY KEY (scope, key)
);
CREATE TABLE IF NOT EXISTS proposals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  requester TEXT NOT NULL,
  account_key TEXT NOT NULL,
  persona TEXT NOT NULL,
  input_prompt TEXT,
  draft_text TEXT,
  media_refs TEXT,
  status TEXT NOT NULL,     -- 'draft','approved','posted','canceled'
  created_at INTEGER NOT NULL
);
'''

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        for stmt in SCHEMA.strip().split(';'):
            if stmt.strip():
                conn.execute(stmt)

def save_tokens(discord_id, account_key, twitter_user_id, screen_name, access_token, refresh_token, expires_in):
    expires_at = int(time.time()) + int(expires_in) - 60
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
        INSERT INTO user_tokens (discord_id, account_key, twitter_user_id, screen_name, access_token, refresh_token, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(discord_id, account_key) DO UPDATE SET
            twitter_user_id=excluded.twitter_user_id,
            screen_name=excluded.screen_name,
            access_token=excluded.access_token,
            refresh_token=excluded.refresh_token,
            expires_at=excluded.expires_at
        ''', (str(discord_id), account_key, twitter_user_id, screen_name, access_token, refresh_token, expires_at))

def get_tokens(discord_id, account_key):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute('''
        SELECT twitter_user_id, screen_name, access_token, refresh_token, expires_at
        FROM user_tokens WHERE discord_id=? AND account_key=?
        ''', (str(discord_id), account_key)).fetchone()
        if not row:
            return None
        return {
            'twitter_user_id': row[0],
            'screen_name': row[1],
            'access_token': row[2],
            'refresh_token': row[3],
            'expires_at': row[4],
        }
