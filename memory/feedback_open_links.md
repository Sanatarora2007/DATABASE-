---
name: Always open links in browser, never just paste them
description: When sharing a URL, always open it in Chrome via browser tools — never just give the link as text
type: feedback
---

Always open links in Chrome using browser tools. Never just paste a URL as text and expect Sanat to click it himself.

**Why:** He explicitly said "don't forget to open them, never" — he wants the browser opened for him, not handed a link to click.

**How to apply:** When a link requires Sanat's presence and input (e.g. API consoles, sign-up flows, dashboards where he needs to click/fill things), open it using Bash `open "https://..."`. Don't open links that are purely informational or that Claude can handle programmatically. Never just paste a URL as text when his action is needed.
