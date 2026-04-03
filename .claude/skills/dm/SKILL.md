---
name: dm
description: "Fetches latest WhatsApp messages using MCP or synced SQLite. Trigger on: \"dm\", \"check my dms\", \"whatsapp messages\", \"latest texts\", \"any messages\", \"check whatsapp\", \"new messages\"."
---

# DM — Latest WhatsApp Messages

## Environment Detection

Detect which environment you're in and use the right data source:

**On Mac:**
1. SQLite first: `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite`
2. Fallback: `mcp__whatsapp__list_chats` + `mcp__whatsapp__list_messages`

**On Cloud (Codespaces / Linux):**
1. Synced SQLite: `~/synced-db/ChatStorage.sqlite`
2. If not found, tell user: "⚠️ WhatsApp DB not synced yet — run `~/refresh-db.sh` or check that your Mac is awake."

## SQLite Query Strategy

When using SQLite (local or synced), query the database directly:

```sql
-- Get recent chats with last message
SELECT cs.ZPARTNERNAME, cs.ZLASTMESSAGEDATE, cs.ZMESSAGECOUNTER,
       m.ZTEXT, m.ZFROMJID, m.ZMESSAGEDATE
FROM ZWACHATSESSION cs
LEFT JOIN ZWAMESSAGE m ON m.ZCHATSESSION = cs.Z_PK
WHERE cs.ZLASTMESSAGEDATE > (strftime('%s', 'now') - 86400 - 978307200)
ORDER BY cs.ZLASTMESSAGEDATE DESC
LIMIT 50;
```

- Timestamps: add 978307200 to convert Apple epoch → Unix epoch
- ZFROMJID = NULL means the message is from the user (outgoing)
- ZPARTNERNAME = contact/group name
- For contacts table (phone numbers): use ContactsV2.sqlite → ZWAADDRESSBOOKCONTACT

## Steps

1. Detect environment (check if Mac SQLite path exists, then synced path, then MCP)
2. Pull recent chats sorted by last activity
3. For each of the top 10 chats, get the latest 3–5 messages
4. Present results as a clean, scannable list

## Output Format

For each chat with recent messages:

- 💬 **[Chat name]** — [timestamp of last message]
  - **[Sender]:** [message text]
  - **[Sender]:** [message text]
  - _(and so on for up to 3–5 messages)_

Group chats and DMs together, sorted by most recent first.

If a chat has unread messages, mark it with 🔴.

For **direct chats**, hyperlink the sender's name: `[Sender Name](whatsapp://send?phone=PHONENUMBER)` (no + prefix, just digits e.g. `919821312060`).

If a message contains a URL, always display it as a clickable markdown hyperlink on its own line, attributed to the sender. Use context from the surrounding message to create a meaningful link label — never use the raw URL as the label.

Keep it tight — no filler, no narration. Just the messages.
