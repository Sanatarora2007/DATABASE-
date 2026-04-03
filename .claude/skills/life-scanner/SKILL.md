---
name: life-scanner
description: "Five-source daily intelligence brief: cross-references Gmail, Calendar, Reminders, WhatsApp (Bulletin + chats via MCP), and Moodle to produce a conflict-aware, ADHD-conscious plain-text action brief. Trigger on: \"scan my life\", \"brief me\", \"what's going on\", \"check everything\", \"what should I be doing\", \"what's coming up\", \"any conflicts\", \"cross-reference my schedule\", \"what am I missing\", \"full picture\", \"check my stuff\", \"daily brief\", \"anything urgent\", \"what's on my plate\", \"update me\". Also trigger proactively when the user asks about tasks, schedule, or to-dos — the value is in the cross-reference, not any single source. This is the orchestrator that reads every source, synthesizes, and delivers one actionable document."
---

# Life Scanner — Daily Intelligence Brief

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

## ENVIRONMENT DETECTION

Before pulling data, detect which environment you're running in:

**Mac (local):** Check if `mcp__apple-events__calendar_events` is available. If yes → Mac mode. All MCPs are available, use SQLite-first strategy per CLAUDE.md.

**Cloud (Codespaces / non-Mac):** If Apple Events MCP is not available → Cloud mode. Use cloud-compatible MCPs and synced SQLite databases.

| Source | Mac (local) | Cloud (Codespaces) |
|--------|------------|-------------------|
| Calendar | SQLite first (`~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb`), then `mcp__apple-events__calendar_events` | Synced SQLite at `~/synced-db/Calendar.sqlitedb`. Fallback: `mcp__claude_ai_Google_Calendar__gcal_list_events` |
| Gmail | `mcp__claude_ai_Gmail__gmail_search_messages` | `mcp__claude_ai_Gmail__gmail_search_messages` |
| WhatsApp | SQLite first (`~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite`), then `mcp__whatsapp__list_messages` | Synced SQLite at `~/synced-db/ChatStorage.sqlite`. If not available, note "⚠️ WhatsApp unavailable — Mac offline or sync not configured" |
| Reminders | SQLite first (`~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Reminders.sqlite`), then `mcp__apple-events__reminders_tasks` | Synced SQLite at `~/synced-db/Reminders.sqlite`. If not available, note "⚠️ Reminders unavailable — check Apple Reminders on your phone" |
| Moodle | Chrome MCP (optional) | Skip — note "⚠️ Moodle requires browser on Mac" |
| Calendar writes | AppleScript via `mcp__macos-automator__execute_script` | `mcp__claude_ai_Google_Calendar__gcal_create_event` |
| Reminder writes | `mcp__apple-events__reminders_tasks` create | Skip — suggest user add manually on phone |

---

## PHASE 1: SILENT DATA PULL

Pull from all sources before writing anything. Do not narrate the extraction process to the user.

**Parallelism plan — launch these concurrently in a single message wherever possible:**
- **Batch 1 (fire simultaneously):** Calendar read + Reminders "Journey" read (Mac only) + Reminders "ATTENDANCE" read (Mac only) + Gmail search_messages. These are independent calls — launch them all in the same tool-call message.
- **Batch 2 (can overlap with Batch 1):** WhatsApp — SQLite query on Mac, synced SQLite on cloud, or WhatsApp MCP fallback.
- **Batch 3 (after Batch 1 returns):** For each promising subject from Batch 1's Gmail results, use `gmail_read_message` to read full body.

**Batch 3 notes — Moodle access (optional, Mac only):** Moodle access requires Chrome/browser navigation. Skip on cloud. On Mac, optional — if WhatsApp Bulletin announcements already surface all critical deadlines, skip Moodle.

**Reuse Phase 1 data for deduplication:** The calendar and reminders data pulled here serves double duty — it feeds the brief AND acts as the deduplication reference for Phase 3. Do NOT re-read calendar/reminders in Phase 3. Store the Phase 1 results internally and reference them when creating events later.

### Source 1: Calendar

**On Mac:**
- Use Apple Calendar SQLite first: `~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb`
- Fallback: `mcp__apple-events__calendar_events` with action `read`

**On Cloud:**
- Check if synced SQLite exists at `~/synced-db/Calendar.sqlitedb`
- If yes: query it using the same SQLite strategy as Mac (CalendarItem table, add 978307200 to timestamps)
- If no: fallback to `mcp__claude_ai_Google_Calendar__gcal_list_events`
- Cover today through +14 days

- Pull from ALL calendars — do not filter. The user's CLAUDE.md specifies routing rules (Calendar = general, EXAMS = tests, DAILY = routine), but read from all of them
- Extract: event title, start/end times, location, calendar name, notes

### Source 2: Gmail (same on Mac and Cloud)
- Use `mcp__claude_ai_Gmail__gmail_search_messages` with queries: "opportunity", "event", "workshop", "deadline", "register", "invitation", "assignment", "submission"
- Limit results to 50 messages
- For each promising subject, use `mcp__claude_ai_Gmail__gmail_read_message` to read the full body
- **Check reply status**: Look at the email thread. If the user has already replied, mark it as handled. Only flag genuinely unresolved messages as action items.
- Extract: sender, subject, full body text, date, CC list, reply status, actionability

### Source 3: WhatsApp

**On Mac:**
- SQLite first: `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite`
- Query ZWAMESSAGE + ZWACHATSESSION for messages from last 7 days
- Search for "Plaksha Bulletin" group and recent high-signal chats
- Fallback: `mcp__whatsapp__list_chats` + `mcp__whatsapp__list_messages`

**On Cloud:**
- Check if synced SQLite exists at `~/synced-db/ChatStorage.sqlite`
- If yes: query it the same way as Mac SQLite
- If no: skip WhatsApp and note "⚠️ WhatsApp data unavailable — run /life-scanner from Mac or ensure SQLite sync is active"

- **First**: Search for "Plaksha Bulletin" or check the returned chats for high-signal Bulletin announcements (events, opportunities, deadlines)
- **Then**: Check other recent group chats — filter by name patterns matching class groups, project teams, clubs, or any group mentioning events or deadlines
- **Check reply status**: Review the returned messages to see if the user has already sent a reply in that chat. If replied, note it as handled.
- Extract: chat name, sender, full message text, timestamp, actionability

### Source 4: Reminders

**On Mac:**
- Use `mcp__apple-events__reminders_tasks` with action `read`
- **Tasks**: filterList = "Journey" (the user's primary task list)
- **Attendance**: filterList = "ATTENDANCE" (attendance tracking)
- For Journey: extract title, due date, priority, completion status, notes
- For Attendance: extract all entries to calculate per-subject attendance percentages
- Flag: overdue tasks (due date < today), high-priority tasks, tasks with no date that relate to upcoming events

**On Cloud:**
- Check if synced SQLite exists at `~/synced-db/Reminders.sqlite`
- If yes: query ZREMCDSAVEDREMINDER table (ZTITLE, ZDUEDATE, ZPRIORITY, ZCOMPLETED, ZDISPLAYDATEDATE columns). Join with ZREMCDBASELIST to filter by list name ("Journey", "ATTENDANCE").
- If no: note "⚠️ Reminders unavailable — check Apple Reminders on your phone"

### Source 5: Moodle (dle.plaksha) — Mac only
- Use Chrome MCP tools to navigate to dle.plaksha.edu.in (Mac only)
- Check the dashboard or upcoming events for: assignment deadlines, new submissions, course announcements
- If Moodle login is required and not active, note that Moodle data couldn't be pulled and flag it
- Extract: assignment names, due dates/times, submission status, course name
- **On Cloud:** Skip. Note "⚠️ Moodle requires browser — run from Mac."

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

## PHASE 3: AUTO-SYNC — Calendar & Reminders

This phase runs after the brief is written. It has two modes:

1. **Mandatory items** (deadlines, confirmed meetings, action-item reminders) get added automatically — no asking. The user's ADHD means every unnecessary "do you want me to add this?" prompt for obligations is a decision point that drains willpower. Just do it.
2. **Optional events** (workshops, social events, talks, competitions, sports, parties, club activities) get presented to the user via AskUserQuestion first. These are choices, not obligations — the user decides what goes on their calendar.

The brief already synthesized everything from 5 sources. Phase 3 takes that synthesis and makes it real — mandatory items silently, optional items after user selection, all without duplicates.

---

**Step 1 — Build deduplication reference (no re-reading — reuse Phase 1 data)**

Do NOT re-read calendar events or reminders here. Phase 1 already pulled all calendar events (14-day window, all calendars) and all "Journey" reminders. Reuse that data directly.

Build an internal dedup list from the Phase 1 results:
- For each calendar event: normalize the title to lowercase, strip extra whitespace, store date + start time + calendar name
- For each reminder: store title (lowercase) + due date
- An event is considered a duplicate if it matches on **both** date AND a fuzzy title match (e.g., "ILGC Project Plan" matches "ILGC Project Plan deadline", "MoU Worksheet" matches "MoU Lab-8 Graded Worksheet"). Use reasonable judgment — err on the side of NOT creating duplicates rather than double-booking.
- As you create events in Steps 2a/2b, add each newly created event to this dedup list so later steps in the same Phase 3 run don't duplicate what earlier steps just created.

---

**Step 2a — Auto-add MANDATORY time-bound items to Calendar (no asking)**

These are non-optional commitments with clear dates/times that get added silently. The user should never be asked about these — they're obligations, not choices:

- **Assignment/submission deadlines** from Moodle and Mail → route to **EXAMS** calendar
- **Meetings already confirmed** (Dr. Shalini, Prof. Brainard, team meetings, scheduled calls) → route to **Calendar**
- **Non-negotiable daily blocks** — Gym, Research (Bloom's Taxonomy), and Marketing (AgriGuru) — get added to the DAILY calendar for every day in the 7-day structural map, automatically. No asking. Use the specific free-window time slots you already computed in the Week Ahead section. If a block had no clean window on a given day (you marked it "❌ No clean 2-hr window" or "❌ Displaced by..."), skip creating it for that day and note it in the confirmation summary.

**Hybrid approach — reading vs writing:**

**On Mac:**
- **Reading** calendar events (Phase 1, deduplication): Use Apple Calendar SQLite or `mcp__apple-events__calendar_events` with action `read`.
- **Writing** calendar events (creating new events): Use `mcp__macos-automator__execute_script` (AppleScript). The Apple Events MCP rejects emojis in titles, but AppleScript supports full Unicode. Use AppleScript for ALL event creation so every event gets an emoji title.

**On Cloud:**
- **Reading**: Already done via `mcp__claude_ai_Google_Calendar__gcal_list_events` in Phase 1.
- **Writing**: Use `mcp__claude_ai_Google_Calendar__gcal_create_event`. Emojis work natively in Google Calendar titles. Route to the equivalent Google Calendar (map "EXAMS" → "EXAMS", "DAILY" → "DAILY", "Calendar" → primary calendar). If those calendars don't exist in Google Calendar, create events on the primary calendar with a prefix tag like `[EXAMS]` or `[DAILY]` in the title.

**AppleScript template — BATCH multiple events in a single call:**

Creating events one at a time means one `osascript` process per event — slow when you're adding 20+ events. Instead, batch all events for the same calendar into a single AppleScript call. Group events by target calendar (DAILY, EXAMS, Calendar) and create all events for that calendar in one script:

```applescript
tell application "Calendar"
    tell calendar "DAILY"
        make new event at end of events with properties {summary:"🏋️ Gym", start date:date "Saturday, 28 March 2026 at 07:00:00", end date:date "Saturday, 28 March 2026 at 08:00:00", description:"Non-negotiable."}
        make new event at end of events with properties {summary:"🔬 Blooms Taxonomy Research", start date:date "Saturday, 28 March 2026 at 08:00:00", end date:date "Saturday, 28 March 2026 at 10:00:00", description:"Deep work block."}
        make new event at end of events with properties {summary:"📱 AgriGuru Marketing", start date:date "Saturday, 28 March 2026 at 13:00:00", end date:date "Saturday, 28 March 2026 at 15:00:00", description:"Marketing block."}
    end tell
    tell calendar "EXAMS"
        make new event at end of events with properties {summary:"🚨 MoU Worksheet DEADLINE", start date:date "Wednesday, 1 April 2026 at 23:00:00", end date:date "Wednesday, 1 April 2026 at 23:59:00", description:"Submit by 11:30 PM."}
    end tell
end tell
```

This creates all events in one process spawn instead of many. Build the full script dynamically — collect all events from Steps 2a and 2b, group by calendar, generate the script, execute once. Fire separate scripts per calendar group if needed (e.g. one for DAILY blocks, one for EXAMS deadlines, one for Calendar meetings) — even 3 calls is far better than 20.

**AppleScript safety notes:** Escape double quotes in titles and notes with backslash (\\"). Date format must match macOS locale — use "Weekday, DD Month YYYY at HH:MM:SS" (e.g. "Friday, 27 March 2026 at 16:00:00"). If a batch AppleScript call fails, fall back to individual `mcp__apple-events__calendar_events` calls without emoji as a safety net — slower but reliable.

**Emoji guide for calendar events — every event gets a contextual emoji at the start of its title:**

| Event type | Emoji | Example title |
|---|---|---|
| Gym | 🏋️ | "🏋️ Gym" |
| Research (Bloom's) | 🔬 | "🔬 Blooms Taxonomy Research" |
| Marketing (AgriGuru) | 📱 | "📱 AgriGuru Marketing" |
| Assignment/submission deadline | 🚨 | "🚨 MoU Lab-8 Worksheet DEADLINE" |
| Exam/test | 📋 | "📋 PDS Test 3" |
| Meeting (Dr. Shalini, Prof. Brainard, team) | 🤝 | "🤝 Dr. Shalini Session" |
| Workshop/talk | 🎤 | "🎤 TEDx PlakshaUniversity" |
| Competition/hackathon | 🏆 | "🏆 Trifecta Business Summit" |
| Sports event/intra | 🏓🏸🏀 | "🏓 Table Tennis Intra" (match sport) |
| Social/party | 🎉 | "🎉 Barrio Bday Bash" |
| Dance/cultural | 💃 | "💃 Bolly Hop Workshop" |
| Registration deadline | 🔗 | "🔗 Register for TT Intra" |
| Generic campus event | 📅 | "📅 Campus Event Name" |

Pick the most specific emoji that matches the event's nature. When in doubt, use 📅 for events and 🚨 for deadlines.

**Emoji guide for Reminders (Apple Reminders MCP supports emojis in titles natively — no AppleScript needed):**

| Task type | Emoji | Example title |
|---|---|---|
| Email follow-up | 📧 | "📧 Follow up with Gurpreet Singh" |
| Assignment submission | 📝 | "📝 Submit ILGC Project Plan" |
| Registration/sign-up | 🔗 | "🔗 Register for TT Intra" |
| Urgent/overdue | 🚨 | "🚨 Email D&I prof about late assignments" |
| Check inbox/waiting | 📬 | "📬 Check CPC Summer Internship inbox" |
| Prep work/study | 📖 | "📖 Prepare handwritten PHY notes" |
| Creative task (reel, edit, content) | 🎬 | "🎬 SCRIPT for REEL" |
| Tech setup | ⚙️ | "⚙️ Setup Opal Mac" |
| Meeting prep | 🤝 | "🤝 Prep for Dr. Shalini session" |
| Generic task | ✅ | "✅ Clean your room" |

**Non-negotiable block titles, times, and notes:**

- **Gym** → title: "🏋️ Gym" | time: 07:00–08:00 | skip if a fixed event starts before 08:00 | calendar: **DAILY** | note: "Non-negotiable. Nothing starts before this."
- **Blooms Taxonomy Research** → title: "🔬 Blooms Taxonomy Research" | time: any free 2-hour window that fits the day's schedule — no fixed preferred time, just pick the best unoccupied 2-hour slot available (e.g. 16:00–18:00 after classes, 09:00–11:00 on free mornings, or wherever a clean 2-hour block exists) | calendar: **DAILY** | note: "Deep work block. 2hrs with Prof Brainard Prince. No interruptions."
- **AgriGuru Marketing** → title: "📱 AgriGuru Marketing" | time: any free 2-hour window — 20:30–22:30 is preferred if available, but if that slot is taken, use any other free 2-hour block during the day. The key constraint is: pick a slot that doesn't overlap with anything, not a specific hour. | calendar: **DAILY** | note: "Marketing block — captions, strategy, content for AgriGuru." If the slot is displaced due to a deadline that night, add the deadline as context in the note (e.g. "ILGC Project Plan due 23:59 tonight — finish it before this block starts").

**Conflict and overlap check (critical — blocks must only go in genuinely free windows):** Before placing ANY Gym/Research/Marketing block on a given day, verify the proposed time slot does not overlap with any existing calendar event — classes, exams, meetings, labs, or other DAILY events already on the calendar. Cross-reference against the full event list from Step 1. If the proposed slot conflicts with an existing event, find the next best free window on that day that is at least 2 hours long (1 hour for Gym). If no conflict-free window exists on that day, skip creating the block entirely and log it in the confirmation summary as "skipped — no free slot on [date]."

**Deduplication for non-negotiable blocks:** A block is a duplicate if an event with a fuzzy title match (e.g. "Gym", "Research", "Blooms", "Marketing", "AgriGuru") already exists on that calendar date at a similar time. If a duplicate is found, skip silently.

For each mandatory deadline/meeting item:
1. Check the deduplication list from Step 1. If a matching event already exists on the same date, **skip it**.
2. If no duplicate found AND the item has a clear date and time, create it via AppleScript with the appropriate emoji prefix from the table above.
3. If AppleScript fails, fall back to `mcp__apple-events__calendar_events` with action `create` (without emoji) and note the fallback in the confirmation summary.
4. If the item has a date but no time (e.g., "registration deadline — March 30"), create an all-day event on the EXAMS calendar or a reminder instead.
5. If the item is missing both date AND time, do NOT create a calendar event — create a reminder in Step 3 instead.

**Routing rules for mandatory items:**
- Tests, exams, assignments, submission deadlines → **EXAMS** calendar
- Confirmed meetings → **Calendar**
- Gym, Research, Marketing daily blocks → **DAILY** calendar

---

**Step 2b — Ask about OPTIONAL events before adding to Calendar**

These are discretionary events — things the user might or might not attend. Workshops, social gatherings, talks, competitions, sports intras, dance sessions, parties, hackathons, club events, etc. The user needs to decide whether they're going before these go on the calendar.

Use `AskUserQuestion` with `multiSelect: true` to present all optional events surfaced in the brief. Group into questions of up to 4 options each. Each option:
- **label**: Event name + date (concise, e.g. "TEDx — Sun Mar 29")
- **description**: Time, venue, and one-line honest assessment of whether it's worth the user's time given their current schedule/attendance/workload

Wait for the user's selections. Then for each selected event:
1. Check the deduplication list from Step 1. If already in the calendar, **skip it** and note it in the confirmation.
2. If not a duplicate, create it using `mcp__apple-events__calendar_events` with action `create`.

**Routing rules for optional items:**
- General events, social gatherings, competitions → **Calendar**
- Routine/campus activities, workshops, sports → **DAILY**

If there are zero optional events surfaced in the brief, skip this step entirely — don't ask an empty question.

**AskUserQuestion constraints:** Max 4 questions per call, max 4 options per question. If more than 4 optional events, split across multiple questions within the same call (up to 4 questions). If more than 16 items total, batch into multiple AskUserQuestion calls.

---

**Step 3 — Auto-add untracked action items to Reminders**

Compile every actionable task, follow-up, or registration surfaced in the brief that is NOT already in the "Journey" reminders list:

- Unresolved email action items (e.g., "follow up with Gurpreet Singh", "email D&I prof about late submissions")
- Registration deadlines for events
- Follow-ups flagged in WhatsApp chats
- Overdue Moodle submissions that need attention (e.g., "check if prof accepts late submission")
- Any task from Claude's Take that has a concrete action attached

For each item:
1. Check the existing "Journey" reminders for a match. If already tracked, **skip it**.
2. **On Mac:** If not tracked, create it using `mcp__apple-events__reminders_tasks` with action `create`, targetList "Journey".
3. **On Cloud:** Cannot create Apple Reminders remotely. Instead, output a clearly formatted "📱 ADD TO REMINDERS" section at the end of the brief listing each task with title, due date, and priority so the user can add them on their phone.
4. Assign a due date based on urgency (today for urgent, next business day for follow-ups, the actual deadline date for submissions).
5. Set priority: HIGH (priority 1) for overdue or same-day items, MEDIUM (priority 5) for this-week items, NONE (priority 0) for nice-to-haves.
6. Assign to the most contextually appropriate section within "Journey". If ambiguous, assign to the top of the list.

---

**Step 4 — Confirmation summary**

After all writes are complete, output a single compact summary at the end of the brief:

```
📥 **SYNCED:**
- 📅 Auto-added to Calendar: [list of mandatory items added — deadlines, meetings — or "Nothing new"]
- 🎪 User-selected events added: [list of optional events the user chose to add, or "None selected"]
- ✅ Auto-added to Reminders: [list of task names added, or "Nothing new — all already tracked"]
- ⏭️ Skipped (duplicates): [count] items already in your calendar/reminders
```

The mandatory items are already added — no approval needed. Optional events were only added after the user selected them. If the user wants to remove anything, they can say so and you'll delete it.

---

**Edge cases:**
- If an MCP write fails, generate the exact structured text (Event Name, Date, Time, Location, Calendar) so the user can copy-paste manually. Don't silently fail.
- If a calendar event has conflicting details across sources (e.g., different times in Mail vs WhatsApp), use the conflict resolution precedence from Execution Rules (Mail > WhatsApp for official logistics, WhatsApp > Mail for same-day urgent changes) and add a note in the event description flagging the discrepancy.
- Never create duplicate events. When in doubt, skip rather than double-book.

---

## EXECUTION RULES

1. **Speed**: Pull all five sources before writing anything. Parallel reads wherever possible.
2. **No narration during pull**: Don't say "Now checking Calendar..." — just pull and then write the brief.
3. **No HTML**: Never. Not once. The brief is text in the chat.
4. **Conflict resolution precedence**: Mail > WhatsApp for official logistics. WhatsApp > Mail for urgent same-day changes (cancellations, room switches).
5. **Reply-status check**: Before flagging any mail or WhatsApp message as an action item, verify the user hasn't already responded. If they have, note "already replied" rather than flagging as pending.
6. **ADHD filter**: Surface tasks that look small but have hidden prep. Flag overcommitment. Name invisible deadlines. Don't normalize overwhelm — call it out.
7. **Non-negotiables are sacred**: Gym, research, marketing, and sleep cutoff are not suggestions. If the day's events displace any of them, say so explicitly and propose a specific recovery slot.
8. **Auto-sync is default for mandatory items**: Phase 3 runs automatically for deadlines, confirmed meetings, and reminders — no asking. But optional events (workshops, social events, talks, competitions, sports, parties) always get presented via AskUserQuestion before being added to the calendar. The user decides what goes on their calendar for discretionary stuff; the system handles obligations silently.
9. **Deduplication is non-negotiable**: Every write operation must be preceded by a read. Fuzzy-match titles + exact-match dates. When in doubt, skip.
