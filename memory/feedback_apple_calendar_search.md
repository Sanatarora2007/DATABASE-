---
name: Apple Calendar Search Strategy
description: Always use SQLite directly for Apple Calendar searches except for latest/recent events
type: feedback
---

Always query the Apple Calendar SQLite database directly for bulk/keyword searches:
`~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb`

Key table: `CalendarItem` — columns: `summary` (title), `start_date`, `end_date` (Core Foundation timestamps, add 978307200 to convert to Unix), `description`, `location_id`
Join: `Location` table on `location_id = Location.ROWID` for location text.

**Why:** The apple-events MCP uses AppleScript which is slow. Direct SQL is instant.

**Rule:**
- Bulk search / keyword / date range / topic search → SQLite directly
- "What's next", "upcoming", recency-sensitive queries → use BOTH SQLite AND apple-events MCP in parallel
- Never default to MCP alone for calendar search tasks

**How to apply:** Any time the user asks to find, search, or look up calendar events, go straight to sqlite3 on Calendar.sqlitedb.
