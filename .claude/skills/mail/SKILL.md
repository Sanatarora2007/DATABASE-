---
name: mail
description: "Fetches recent important Gmail messages from the last 2-3 days using MCP. Trigger on: \"mail\", \"check my mail\", \"gmail\", \"check gmail\", \"any emails\", \"recent emails\", \"missed emails\", \"what's in my inbox\"."
---

# Mail — Recent Important Gmails

Use `mcp__claude_ai_Gmail__gmail_search_messages` to find important recent emails from the last 2-3 days, then `mcp__claude_ai_Gmail__gmail_read_message` to get full details for each.

## Steps

1. Call `mcp__claude_ai_Gmail__gmail_search_messages` with query `newer_than:3d` to get emails from the last 3 days. Limit to 20.
2. Filter for important/actionable emails — skip newsletters, automated notifications, receipts, and promotional mail unless they contain a deadline, registration, or action item.
3. For each important email, call `mcp__claude_ai_Gmail__gmail_read_message` to get the full body.
4. Extract: sender name, date, time, a 1-sentence summary, and any URLs or reference/tracking numbers in the body.
5. Present as a markdown table, sorted by most recent first.

## Output Format

Present results as a markdown table:

| # | Sender | Date & Time | Summary | Link / Ref |
|---|--------|-------------|---------|------------|
| 1 | Sender Name | Mar 28, 12:30 PM | [**Email Subject**](https://mail.google.com/mail/u/0/#all/MESSAGE_ID) — One-sentence summary of what the email is about and what action (if any) is needed. | [Descriptive Label](URL) or Ref: XXXX |

**Summary column rules:**
- Always hyperlink the email subject/title to the direct Gmail URL: `https://mail.google.com/mail/u/0/#all/{messageId}`
- Format: `[**Subject**](gmail_url) — summary sentence`
- The Gmail link uses the messageId returned by the API

**Link / Ref rules:**
- If the email contains a URL, display it as a clickable markdown hyperlink: `[Descriptive Label](URL)`
- Use context from the email to create a meaningful label (e.g., "Submit Assignment", "Join Meeting", "Register Here", "Track Order") — never use the raw URL as the label
- If the email contains a reference number, ticket number, or tracking number, display it as `Ref: XXXX`
- If both a link and a ref exist, show both separated by a line break
- If neither exists, leave the cell empty

**Importance filter — include:**
- Emails from professors, university admin, supervisors, or known contacts
- Deadlines, assignments, submissions, exam notices
- Event invitations, registrations, opportunities
- Any email requiring a reply or action

**Skip:**
- Newsletters, promotional mail, automated receipts
- Social notifications (LinkedIn, Instagram, etc.)
- Anything clearly no-action-needed

If inbox is clear: "✅ No important emails in the last 3 days."
