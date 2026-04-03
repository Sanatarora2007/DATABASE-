---
name: imp
description: "Quick today-only priority brief: checks WhatsApp, Apple Calendar, Apple Reminders, and Gmail and reports only what needs to get done TODAY. Trigger on: \"/imp\", \"what's important today\", \"what do I need to do today\", \"today's priorities\", \"quick brief\"."
---

# /imp — Today's Priorities

Pull from four sources and report ONLY what matters today. No week-ahead, no deep analysis. Fast, ruthless, today-focused.

**CRITICAL: Always use Gmail (mcp__claude_ai_Gmail__*). Never Apple Mail.**

---

## SILENT DATA PULL

Pull all four sources before writing anything. No narration during pull.

### 1. Gmail
- Use `mcp__claude_ai_Gmail__gmail_search_messages` with query: `is:unread after:{{today}}`
- For each promising message, use `mcp__claude_ai_Gmail__gmail_read_message` to get the body
- Only flag messages that require action TODAY

### 2. Apple Calendar
- Use `mcp__apple-events__calendar_events` with action `read`, today's date only
- Pull from ALL calendars
- Extract every event happening today with start/end times

### 3. Apple Reminders
- Use `mcp__apple-events__reminders_tasks` with action `read`, filterList = "Journey"
- Extract: overdue tasks + tasks due today only

### 4. WhatsApp
- Use `mcp__whatsapp__list_chats` to get recent chats
- Use `mcp__whatsapp__list_messages` on the most recent active chats (last 24 hours)
- Look for anything time-sensitive or requiring a reply today

---

## OUTPUT FORMAT

Plain text in chat. Short. Scannable. No HTML, no files.

```
📅 TODAY — [Day, Date]

📧 GMAIL — Action needed
• [Sender] — "[Subject]" → [what to do]
• (or) ✅ Nothing urgent

📆 CALENDAR — Today's schedule
• [Time] — [Event]
• [Time] — [Event]

✅ REMINDERS — Due/overdue today
• 🔴 OVERDUE: [Task]
• 🟡 DUE TODAY: [Task]
• (or) ✅ Nothing due today

💬 WHATSAPP — Needs a reply
• [Chat] — [what they said / what's needed]
• (or) ✅ Nothing urgent

⚡ TOP 3 THINGS TO DO RIGHT NOW
1. [Most urgent]
2. [Second]
3. [Third]
```

Keep "Top 3" ruthlessly honest — what MUST happen today, not what would be nice.
