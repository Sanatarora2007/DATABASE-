# MCP Sources — Sanat's Claude Setup

These are the MCP servers connected to Claude Code. Re-enable them via Claude Code → Settings → Connected Sources.

---

## Connected via Claude.ai (OAuth / built-in)

| MCP | What it does |
|-----|-------------|
| **Gmail** | Read, search, draft Gmail messages |
| **Google Calendar** | Read/create/update Google Calendar events |
| **Canva** | Create and edit Canva designs |

---

## Connected via Claude Code Extension

| MCP | What it does | Notes |
|-----|-------------|-------|
| **Claude in Chrome** | Browser automation, read pages, click, fill forms, screenshot | Required for WhatsApp web, browsing |
| **WhatsApp** | Send/receive WhatsApp messages, read chats | Runs via Chrome extension |
| **Apple Events** | Read Apple Calendar + Reminders | Local Mac MCP |
| **Apple Mail** | Read/send Apple Mail | Local Mac MCP |
| **Google Maps** | Directions, geocoding, place search | |
| **macOS Automator** | Run AppleScript/shell scripts on Mac | Used for system-level automation |
| **Music** | Control Apple Music, search, queue | config: `mcp.json` |
| **Playwright** | Headless browser automation | config: `.mcp.json` |

---

## Config Files (auto-synced via symlinks)

- `.claude/.mcp.json` → Playwright
- `mcp.json` → Music

---

## Notes

- WhatsApp SQLite path: `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite`
- Apple Calendar SQLite: `~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb`
- Always use SQLite directly for WhatsApp and Calendar — MCP is fallback only
