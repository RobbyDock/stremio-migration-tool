<img width="1200" height="300" alt="image" src="https://github.com/user-attachments/assets/391b6b7d-3d32-47b8-84be-a441f489c1ce" />

# Stremio Library & Addon Migration

A tiny, click-and-play tool for moving your Stremio library (watched/saved titles + progress) and installed addons from one account to another — useful since Stremio doesn't officially support changing an account's email.

## How it works

`index.html` is a single self-contained file — no install, no build step, no server. It talks directly to Stremio's own API (`api.strem.io`) from your browser. Your credentials and library data never leave your machine except to hit Stremio's servers directly, exactly like the official Stremio app does.

## Usage

1. Double-click `index.html` to open it in your browser.
2. **Source account (old)**: enter the email/password of the account you're migrating *from*, then click **Log in & fetch library + addons**. It'll show how many library items and addons it found, plus a "Download backup JSON" link you can save as a safety net. Alternatively, click **Import a backup JSON file instead** to load a previously downloaded backup without logging in again.
3. **Destination account (new)**: enter the email/password of the account you're migrating *to*, then click **Log in**.
4. Click **Migrate library + addons →**. This pushes the fetched library items and addon collection to the destination account.

Re-running the migration is safe — library items keep their original IDs, so re-migrating overwrites rather than duplicates.

## Data validation

Every time the source library is loaded (via login or file import), the tool checks for duplicate IDs, invalid/empty `_mtime`/`_ctime` timestamps, and missing required fields, and shows a report. Items with invalid/empty timestamps are automatically sanitized (given a valid timestamp) before they're offered for backup or migration — Stremio's client can fail to load a library that contains one of these, so this is applied unconditionally.

## Notes

- Nothing is written to disk automatically. The only file you can save is the backup JSON, and only if you click that link yourself.
- This uses Stremio's unofficial but stable web API (the same one the official apps and community tools like Stremio Addon Manager use), not a documented public API — if Stremio changes it, this tool may need updating.
