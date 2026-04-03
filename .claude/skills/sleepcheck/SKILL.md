---
name: sleepcheck
description: "Check if Mac sleep is disabled or enabled, then ask to turn it on, off, or leave as is. Trigger on: \"/sleepcheck\", \"check sleep\", \"is sleep disabled\", \"sleep status\"."
---

# Sleep Check

Run `pmset -g` and extract the `SleepDisabled` value. Then:

1. Report clearly: "Sleep is currently **disabled** (Mac won't sleep)" or "Sleep is currently **enabled** (Mac can sleep normally)"
2. Ask the user: "Would you like to turn sleep **on**, **off**, or leave it as is?"
3. Based on their answer:
   - "on" → run `sudo pmset -a disablesleep 0`
   - "off" → run `sudo pmset -a disablesleep 1`
   - "leave it" / "none" / anything else → do nothing, confirm no changes made
