---
name: reply
description: "Send a WhatsApp message to a contact. Trigger on: \"reply to [person]\", \"send [person]\", \"message [person] on whatsapp\", \"tell [person] on whatsapp\", \"whatsapp [person]\"."
---

# Reply — Send WhatsApp Message

Send a WhatsApp message to a contact. Copy the user's text exactly — no spell-fixing, no grammar corrections, no changes whatsoever. Square bracket sections like `[do something]` or `[write something here]` are instructions from the user for you to fulfill — replace them with appropriate text, then compose the final message.

## Steps

### 1. Parse the input
- Extract the **recipient name** from the command (e.g., "reply to Saurabh Sir" → recipient = "Saurabh Sir")
- Extract the **message body** — everything the user typed as the message content
- For any `[...]` sections in the message: treat them as inline instructions. Generate appropriate text to replace them. Do NOT alter any text outside brackets.

### 2. Find the contact's chat JID
- Call `mcp__whatsapp__search_contacts` with the recipient name to find their phone number / JID.
- If multiple results, pick the most likely match based on context (saved name, recent chat history).
- If ambiguous, ask the user to clarify before proceeding.
- To get the correct `chat_jid`, call `mcp__whatsapp__get_direct_chat_by_contact` using the contact's JID, OR match against recent chats from `mcp__whatsapp__list_chats`.

### 3. Show the composed message and ask permission
Present the final message clearly:

---
**To:** [Recipient name]
**Message:**
[exact final message text]

Send this? (y/n)

---

STRICTLY wait for the user to respond with y/n before doing anything. Do not send without explicit confirmation. This is non-negotiable.

### 4. On confirmation (y)
- Call `mcp__whatsapp__send_message` with the correct `chat_jid` and the final message text.
- Confirm: "Sent."

### 5. On rejection (n)
- Ask: "What would you like to change?"

## Error Handling

WhatsApp MCP can fail intermittently. If `send_message` fails or returns an error, attempt the following in order before asking the user for help:

1. **Re-fetch the chat JID** — the JID used may be stale. Call `mcp__whatsapp__list_chats` or `mcp__whatsapp__get_direct_chat_by_contact` again to get a fresh JID and retry.
2. **Check JID format** — DMs must use `[phone]@s.whatsapp.net`, groups use `[id]@g.us`. Verify format is correct.
3. **Retry once** — call `send_message` a second time with the corrected JID.
4. **If still failing** — report the exact error to the user and ask them to check if WhatsApp is open and connected on their Mac.

Never silently fail. Always report outcome.

## Rules

- NEVER alter text outside square brackets. Typos, slang, broken grammar — send it as-is.
- NEVER send without y confirmation. Even if the user said "send this" in the original prompt — still show the preview and ask.
- Square brackets `[like this]` = your instructions to fill in. Everything else = sacred.
- If the message has no square brackets, the final message = exactly what the user typed, character for character.
