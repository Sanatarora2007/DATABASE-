---
name: life-scanner-v2
description: "Five-source daily intelligence brief: cross-references Apple Mail, Calendar, Reminders, WhatsApp (Bulletin + chats), and Moodle to produce a conflict-aware, ADHD-conscious plain-text action brief. Trigger on: \"scan my life\", \"brief me\", \"what's going on\", \"check everything\", \"what should I be doing\", \"what's coming up\", \"any conflicts\", \"cross-reference my schedule\", \"what am I missing\", \"full picture\", \"check my stuff\", \"daily brief\", \"anything urgent\", \"what's on my plate\", \"update me\". Also trigger proactively when the user asks about tasks, schedule, or to-dos — the value is in the cross-reference, not any single source. This is the orchestrator that reads every source, synthesizes, and delivers one actionable document."
---

# Life Scanner v2 — Daily Intelligence Brief

You are building a personalized, conflict-aware daily intelligence brief by pulling from five (optionally six) data sources and cross-referencing everything. The output is plain text delivered directly in the chat — not an HTML file, not a summary card. A real, honest, readable brief.

The user this was built for: college student, ADHD (medicated), high-output when locked in, invisible when not. Time-blind on soft deadlines. Hyperfocuses on creative work, drops administrative tasks. Needs the brief to do the executive function their brain skips — surfacing what's actually urgent, what's about to collide, and what they're most likely to underestimate.

**CRITICAL: Output format is plain text only, delivered directly in the chat window. Never create an HTML file, artifact, or any external file for the brief. Every word of the brief lives in the chat itself.**

---

## DAILY NON-NEGOTIABLES

These recurring commitments exist every day and must be accounted for when calculating free windows, identifying conflicts, and building the Week Ahead overview. They are as real as classes — treat them as immovable blocks.

- **7:00 AM — Gym** (at least 3–4 days per week). If the user hasn't been going, note it. If a morning conflict threatens it, flag it.
- **2 hours/day — Bloom's Taxonomy research** (with Prof. Brainard Prince). This is deep work. It needs a protected, uninterrupted slot. When building the day map, explicitly place where this 2-hour block fits given the day's schedule. If there's no clean 2-hour window, say so — don't pretend a fragmented 30-min gap counts.
- **2 hours/day — Marketing work** (AgriGuru, preferably after 8:30 PM). This is the evening work block. Social media captions, strategy, content — it happens best late. When mapping the evening, account for this. If something else (ILGC brainstorm, team meeting, social event) eats the 8:30–10:30 PM window, flag the marketing block as displaced and suggest when it moves to.
- **11:30 PM — Hard sleep cutoff.** Nothing gets scheduled or suggested past this. If the marketing block is pushed late, it ends at 11:30 regardless. If an assignment is "due at midnight," the real deadline is 11:30 PM. Build all evening plans around this wall.

---

## PHASE 1: SILENT DATA PULL

Pull from all sources before writing anything. Do not narrate the extraction process to the user. Launch reads in parallel wherever possible.

### Source 1: Apple Calendar
- Use `mcp__apple-events__calendar_events` with action `read`
- Cover today through +14 days
- Pull from ALL calendars — do not filter. The user's CLAUDE.md specifies routing rules (Calendar = general, EXAMS = tests, DAILY = routine), but read from all of them
- Extract: event title, start/end times, location, calendar name, notes

### Source 2: Apple Mail
- Use `mcp__apple-mail__list_mailboxes` to identify the primary inbox (usually Outlook)
- Use `mcp__apple-mail__list_messages` on the primary inbox, limit 50
- Use `mcp__apple-mail__search_messages` with queries: "opportunity", "event", "workshop", "deadline", "register", "invitation", "assignment", "submission"
- For each promising subject, use `mcp__apple-mail__get_message` to read the full body
- **Check reply status**: Look at the mail thread. If the user has already replied, mark it as handled. Only flag genuinely unresolved messages as action items.
- Extract: sender, subject, full body text, date, CC list, reply status, actionability

### Source 3: WhatsApp (Bulletin + Chats)
- Use Chrome MCP tools to open WhatsApp Web in Chrome
- **First**: Navigate to the pinned "Plaksha Bulletin Announcements" channel (not the general group chat — this is a common mistake; the Announcements channel is pinned separately within the Bulletin community)
- Scroll through recent messages (WhatsApp lazy-loads, so scroll multiple times to get history)
- For poster images: use the `zoom` action to read event details from posters that aren't in the accessibility tree
- For truncated messages: click "Read more" to get full text
- **Then**: Check other recent chats — use the "Unread" filter and "Groups" tab to find high-signal conversations (class groups, project teams, clubs, any group mentioning events or deadlines)
- **Check reply status**: Before flagging any message as requiring action, check whether the user has already replied in that chat. If replied, note it as handled.
- Extract: chat name, sender, full message text, timestamp, reply status, actionability

### Source 4: Apple Reminders
- Use `mcp__apple-events__reminders_tasks` with action `read`
- **Tasks**: filterList = "Journey" (the user's primary task list)
- **Attendance**: filterList = "ATTENDANCE" (attendance tracking)
- For Journey: extract title, due date, priority, completion status, notes
- For Attendance: extract all entries to calculate per-subject attendance percentages
- Flag: overdue tasks (due date < today), high-priority tasks, tasks with no date that relate to upcoming events

### Source 5: Moodle (dle.plaksha)
- Use Chrome MCP tools to navigate to dle.plaksha.edu.in
- Check the dashboard or upcoming events for: assignment deadlines, new submissions, course announcements
- If Moodle login is required and not active, note that Moodle data couldn't be pulled and flag it
- Extract: assignment names, due dates/times, submission status, course name

---

## PHASE 2: WRITE THE BRIEF

Output everything in plain text, directly in the chat message. Do NOT create any files — no HTML, no .md, no artifacts, no documents. The brief IS the chat message. If you catch yourself about to write a file, stop. Type it into the response instead.

Write the brief in this exact structure. Use bullet points and emojis throughout to make scanning fast and intuitive.

---

### 1. 📅 CALENDAR — What's locked in

List every event from the next 14 days grouped by day. Each event is a bullet point:

- 📆 **[Day, Date]**
  - ⏰ [Start–End] — **[Event name]** ([Calendar name])
  - 📍 [Location/Room if known]
  - 📝 [Any critical notes — only if they change what the user needs to do]

Keep it tight — one bullet per event. Only add 📝 notes if genuinely relevant.

---

### 2. 📧 MAIL — What actually needs action

Only include emails that are genuinely unresolved and require the user to do something. Skip auto-confirmations, newsletters, booking receipts.

Each actionable email is a bullet:

- 🔴 **[Sender]** — "[Subject]"
  - 🎯 Action: [what needs to happen and by when]
  - ↩️ Replied: [Yes/No]

If nothing needs action: "✅ Inbox clear of actionable items."

---

### 3. 💬 WHATSAPP — Events + coordination intel

**📢 Bulletin Announcements:** Each event/opportunity as a bullet:

- 🎪 **[Event name]**
  - 📆 [Date] | ⏰ [Time] | 📍 [Venue]
  - 🔗 [Registration link if present]
  - 👥 [Key people/organizers if relevant]
  - 💡 [One-line honest assessment]

**💬 Group Chats:** Surface coordination relevant to upcoming decisions:

- 👥 **[Chat name]** — [Key info: trip plans, meeting times, team assignments, schedule changes]

---

### 4. ✅ REMINDERS — Open loops

**📋 Journey (tasks):** Each incomplete task as a bullet:

- 🔴 (HIGH) / 🟡 (MED) / ⚪ (NONE) **[Task name]**
  - 📆 Due: [date or "no date"]
  - ⏰ Overdue: [Yes ❗ / No]
  - 📝 [Notes if relevant]

**📊 ATTENDANCE:** Each subject as a bullet:

- 🔴 / 🟡 / 🟢 **[Subject]: [X]%** — MAX possible: [Y]% | [Z] classes left
  - Use 🔴 if impossible to reach 75%, 🟡 if barely possible (0 buffer), 🟢 if safe

---

### 5. 📚 MOODLE — Upcoming submissions

Each assignment as a bullet, grouped by status:

**❌ OVERDUE:**
- 🚨 **[Assignment name]** — [Course]
  - 📆 Was due: [date/time] | ✅ Submitted: No

**⏳ UPCOMING:**
- 📝 **[Assignment name]** — [Course]
  - 📆 Due: [date/time] | ✅ Submitted: [yes/no/not yet]

If Moodle data wasn't accessible: "⚠️ Moodle data unavailable — couldn't pull assignments."

---

### 6. ⚡ CONFLICTS & COLLISIONS

This is the most important section. Each conflict is a bullet:

- ⚠️ **CONFLICT:** [Source A] says X — [Source B] says Y
  - ✅ **Resolution:** [what to trust and what to do]

Types to check:
- Time overlaps (event in same slot as class)
- Same event with different details across sources (use mail as source of truth for times/links; WhatsApp for urgent cancellations/room changes)
- Deadline landing during an already-heavy day
- Trip or social plan conflicting with internship, exam, or academic timeline
- Non-negotiable blocks (gym, research, marketing, sleep) being displaced

---

### 7. 🧠 CLAUDE'S TAKE

This is your honest editorial layer. Not a summary — a perspective. What is the user most likely to miss? What looks manageable but isn't? What's the highest-leverage thing they should do in the next 24 hours?

Speak plainly. Don't hedge. Don't soften. ADHD-aware: name the invisible prep requirements, the tasks that look 10 minutes but eat an hour, the overcommitment pattern if it's present.

Limit: 5–7 sentences max. Dense, direct.

---

### 8. 🗓️ WEEK AHEAD — Structural map

For each day in the next 7 days, use this bullet structure:

- 📆 **[Day, Date]**
  - 🔒 **Fixed:** [classes, exams, meetings with times]
  - 🏋️ **Gym:** [7 AM — going/skipped/conflict?]
  - 🔬 **Research (2hr):** [Specific time slot where it fits, e.g. "16:00–18:00" — or "❌ No clean 2-hr window"]
  - 📱 **Marketing (2hr):** [Specific evening slot, e.g. "20:30–22:30" — or "❌ Displaced by [reason]"]
  - 📅 **Deadlines:** [assignments, submissions, responses due]
  - 📝 **Tasks:** [open items from Reminders, follow-ups, prep work]
  - 🟢 **Free windows:** [realistic ones AFTER non-negotiables are placed — not theoretical. Account for initiation lag and transitions]
  - 🚨 **Danger level:** [🟢 Manageable / 🟡 Heavy / 🔴 Overloaded] — [brief reason if yellow or red]

Don't just list non-negotiables abstractly — place them in specific time slots given the day's constraints. 11:30 PM hard cutoff applies to all evening planning. A day where both research and marketing blocks get displaced is a 🔴 — name it.

---

## PHASE 3: INTERACTIVE — Event Interest + Calendar/Reminders

This section is interactive and uses the `AskUserQuestion` tool to collect user selections. Three stages, each using AskUserQuestion with `multiSelect: true`.

**CRITICAL: You MUST use the AskUserQuestion tool for each stage. Do NOT just type questions into the chat and wait — the user needs clickable selection UI. Each stage is a separate AskUserQuestion call.**

**AskUserQuestion constraints:** Max 4 questions per call, max 4 options per question. If you have more than 4 items, split them across multiple questions within the same call (up to 4 questions). If you have more than 16 items total, batch into multiple AskUserQuestion calls.

---

**Stage 1 — 🎪 Optional Events: Are you interested?**

Compile every upcoming optional event surfaced in the brief (workshops, talks, competitions, social events, club activities — anything that is not a class or fixed commitment).

Use `AskUserQuestion` with `multiSelect: true`. Group events into questions of up to 4 options each. Each option:
- **label**: Event name + date (concise, e.g. "TEDx — Sun Mar 29")
- **description**: Time, venue, and one-line honest assessment of whether it's worth the user's time

Example structure:
```
AskUserQuestion({
  questions: [
    {
      question: "Which of these events are you actually going to?",
      header: "Events",
      multiSelect: true,
      options: [
        { label: "TEDx — Sun Mar 29", description: "1:30–4:00 PM, Room 1001. Great speaker lineup, aligns with your creative interests." },
        { label: "Mustafa Workshop — Sun Mar 29", description: "4:30–5:30 PM, Makerspace. Only 40 seats. High value for filmmaking/storytelling." },
        { label: "TT Intra — Apr 7-8", description: "MPH. Fun, but overlaps class days. Given attendance crisis, think carefully." },
        { label: "Barrio Bash — Sat Apr 4", description: "8:30 PM. Saturday night, no classes next day. Mocktails on Avnet. Go." }
      ]
    }
  ]
})
```

If there are more than 4 optional events, use up to 4 questions in the same call to cover all of them.

Wait for user's response before proceeding to Stage 2.

---

**Stage 2 — 📅 Add to Calendar**

Take the user's selections from Stage 1 and combine them with any other time-sensitive items from the brief that are NOT already in their Calendar.

Use `AskUserQuestion` with `multiSelect: true`. Each option:
- **label**: Event name + date
- **description**: Time, and which calendar it routes to (Calendar = general events/meetings, EXAMS = tests/assignments, DAILY = routine activities)

Example:
```
AskUserQuestion({
  questions: [
    {
      question: "Which of these should I add to your Calendar?",
      header: "Calendar",
      multiSelect: true,
      options: [
        { label: "TT Intra — Apr 7-8", description: "MPH. Route to → Calendar" },
        { label: "Barrio Bash — Apr 4 8:30PM", description: "Barrio restaurant. Route to → Calendar" },
        { label: "ILGC Project Plan deadline", description: "Mar 31 11:59 PM. Route to → EXAMS" }
      ]
    }
  ]
})
```

Wait for user's response. Add the selected items using `mcp__apple-events__calendar_events` with action `create`. Always do a read first to check for duplicates. Confirm what was added in one line.

---

**Stage 3 — ✅ Add to Reminders**

Compile every untracked task, follow-up, registration deadline, or action item from the brief that is NOT already in the "Journey" Reminders list.

Use `AskUserQuestion` with `multiSelect: true`. Each option:
- **label**: Task name (concise)
- **description**: Suggested due date and section within "Journey"

Example:
```
AskUserQuestion({
  questions: [
    {
      question: "Which of these should I add to your Reminders (Journey list)?",
      header: "Reminders",
      multiSelect: true,
      options: [
        { label: "Register for Mustafa Workshop", description: "Due: today. Only 40 seats." },
        { label: "Reply to Mom on WhatsApp", description: "Due: today. She sent 3 messages." },
        { label: "Submit overdue D&I assignments", description: "Due: ASAP. Check if prof still accepts late." }
      ]
    }
  ]
})
```

Wait for user's response. Add selected items using `mcp__apple-events__reminders_tasks` with action `create`, targetList "Journey". Confirm what was added.

---

**Routing rules (from CLAUDE.md):**
- Calendar events → route to "Calendar", "EXAMS", or "DAILY" based on context
- Reminders → always go to "Journey" list, assigned to the most appropriate section
- Always read before write — check for duplicates before creating anything
- If missing date/time for a calendar event → stop and ask before writing
- If context is ambiguous for a Reminders section → assign to top of list and ask for categorization

---

## EXECUTION RULES

1. **Speed**: Pull all five sources before writing anything. Parallel reads wherever possible.
2. **No narration during pull**: Don't say "Now checking Calendar..." — just pull and then write the brief.
3. **No HTML**: Never. Not once. The brief is text in the chat.
4. **Conflict resolution precedence**: Mail > WhatsApp for official logistics. WhatsApp > Mail for urgent same-day changes (cancellations, room switches).
5. **Reply-status check**: Before flagging any mail or WhatsApp message as an action item, verify the user hasn't already responded. If they have, note "already replied" rather than flagging as pending.
6. **ADHD filter**: Surface tasks that look small but have hidden prep. Flag overcommitment. Name invisible deadlines. Don't normalize overwhelm — call it out.
7. **Non-negotiables are sacred**: Gym, research, marketing, and sleep cutoff are not suggestions. If the day's events displace any of them, say so explicitly and propose a specific recovery slot.
8. **AskUserQuestion is mandatory for Phase 3**: Never type questions into chat and wait. Always use the `AskUserQuestion` tool with `multiSelect: true` for all three interactive stages. This gives the user clickable checkboxes instead of requiring them to type responses.
9. **AskUserQuestion constraints**: Max 4 questions per call, max 4 options per question. If more items exist, split across multiple questions or multiple calls.
