---
name: Apple Mail Search Strategy
description: Always use SQLite directly for Apple Mail searches except for latest/recent messages
type: feedback
---

**Gmail is primary. Apple Mail is backup only. Never use Apple Mail SQLite.**

**Rule:**
- Any email task → Gmail MCP first, always
- Apple Mail MCP only if Gmail MCP fails or returns no results
- Never query Apple Mail SQLite

**Why:** Sanat confirmed Gmail is the primary source of truth. Apple Mail is a fallback.
