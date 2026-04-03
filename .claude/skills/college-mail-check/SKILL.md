---
name: college-mail-check
description: >
  Scans college email inbox, surfaces only what needs attention sorted by urgency,
  and automatically adds time-sensitive items to Apple Calendar.
  Use this skill whenever the user asks anything like "check my mail",
  "any important emails?", "what do I need to do from my inbox",
  "college email updates", "anything urgent in my email", "what's in my inbox",
  or any similar request to review, triage, or summarize college emails.
  Always use this skill proactively when the user asks about their tasks, schedule,
  or to-dos, since emails often contain the most time-sensitive action items.
---

# College Mail Check Skill

You are helping a college student triage their inbox. The goal is to surface only what **requires action**, present it with full context, and automatically calendar anything time-sensitive so nothing slips.

## Step 1: Get the lay of the land

Call `get_unread_count`, then `list_mailboxes` to find which accounts/folders have unread mail. Focus on the primary college account (typically Outlook for university students).

## Step 2: Pull recent inbox messages

Use `list_messages` on the primary Inbox — fetch the last 30–40 messages (not just unread, since important emails may already have been opened but still need action).

## Step 3: Identify what's actionable

Judge from subject + sender whether each email *might* need action. Then read the full body (`get_message`) **only for potentially actionable ones**. Skip:
- Automated confirmations with no decision needed (e.g. "you submitted your assignment", "booking confirmed")
- Marketing / promotional / welcome emails
- Meeting room acceptances / calendar auto-replies
- General newsletters with no RSVP or deadline

Read the full body for:
- Emails from professors, admin, or department heads asking you to do something
- Exam, assessment, or academic deadline notices
- Event invitations requiring RSVP or registration
- Emails explicitly requesting a reply
- Anything flagged as urgent or containing a named deadline

## Step 4: Extract full details

For every actionable email, extract ALL of the following that are present in the email body:
- **Subject / what it's about**
- **Who sent it** (name + role/relation if clear)
- **Date & time** (when the event/deadline/action is due — not the email's sent date)
- **Duration** (if stated)
- **Location** (room, building, online link, address)
- **Key action required** (what exactly you need to do — attend, reply, register, prepare, etc.)
- **Registration/RSVP link** (if any)
- **Seat or capacity limit** (if stated — signals urgency to register quickly)
- **Any other important notes** from the email

Never truncate or omit these details. The point is to give the user everything they need without having to open the email themselves.

## Step 5: Add time-sensitive items to Apple Calendar

For every item that has a specific date and time (events, meetings, deadlines, in-person visits), create a calendar event using `mcp__apple-events__calendar_events` with `action: "create"`.

First call `mcp__apple-events__calendar_calendars` with `action: "read"` to see available calendars. Use the most appropriate one (e.g. a college/university calendar if it exists, otherwise the default).

For each event, include:
- `title`: clear, descriptive (e.g. "Sports Officer Meeting — Attendance Issue")
- `startDate` and `endDate` (use duration from email if available; default to 1 hour if not stated)
- `location`: from the email
- `note`: paste the key info from the email — who sent it, what it's about, any links or action needed
- `alarms`: set a reminder 30 minutes before (`relativeOffset: -1800`)

Do this silently as part of the workflow — don't ask for permission first, just do it. Report which events were added at the end.

## Step 6: Present the summary

Group actionable items into tiers — only include tiers that have something in them:

**🚨 Today / Time-Sensitive**
Things expiring today or requiring in-person action by end of day.

**📩 Reply Needed**
Emails explicitly waiting for your response. State what the reply should contain if clear from context.

**📅 Upcoming Events / Registrations**
Events, workshops, competitions requiring RSVP or registration. Include: date, time, duration, location, contact/host, registration link, seat limit.

**📚 Academic Prep**
Exam guidelines, assignment rules, grading changes, or anything affecting how you prepare for something.

**⏳ Watch Your Inbox**
Things where you've been told something is coming (e.g. "application link will be sent soon").

At the end of the summary, add a line like:
> 📅 Added X event(s) to your calendar: [event name], [event name]

## Style guidelines

- Be direct — no filler phrases like "Here's a summary of..." Just the information.
- For every item, include: **who**, **what**, **when**, **where**, and **what you need to do**.
- If a deadline is today, make that obvious upfront.
- For registrations with limited seats, highlight the urgency.
- End with a short tally: e.g. "2 things need action today, 3 coming up this week."
- If nothing is actionable, say so clearly.

## What to skip

Do not list emails that don't require action. The user needs to know what to do — not a recap of their whole inbox.
