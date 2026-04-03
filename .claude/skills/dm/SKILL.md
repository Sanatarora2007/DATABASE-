---
name: dm
description: "Fetches latest WhatsApp messages using MCP. Trigger on: \"dm\", \"check my dms\", \"whatsapp messages\", \"latest texts\", \"any messages\", \"check whatsapp\", \"new messages\"."
---

# DM — Latest WhatsApp Messages

Use `mcp__whatsapp__list_chats` to get recent chats, then `mcp__whatsapp__list_messages` on the top chats to surface the latest messages.

## Steps

1. Call `mcp__whatsapp__list_chats` to get the list of chats sorted by last activity.
2. For each of the top 10 chats (or fewer if less exist), call `mcp__whatsapp__list_messages` with a limit of 3–5 to get the latest messages.
3. Present results as a clean, scannable list.

## Output Format

For each chat with recent messages:

- 💬 **[Chat name]** — [timestamp of last message]
  - **[Sender]:** [message text]
  - **[Sender]:** [message text]
  - _(and so on for up to 3–5 messages)_

Group chats and DMs together, sorted by most recent first.

If a chat has unread messages, mark it with 🔴.

If a message contains a URL, always display it as a clickable markdown hyperlink on its own line, attributed to the sender. Use context from the surrounding message to create a meaningful link label (e.g., "Documentary Project Form", "Registration Link", "Meeting Join Link") — never use the raw URL as the label.

Keep it tight — no filler, no narration. Just the messages.
