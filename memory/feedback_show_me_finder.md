---
name: "Show Me" = Reveal in Finder
description: When user says "show me" in context of a file or folder, reveal and select it in Finder without opening it
type: feedback
---

When the user says "show me" (or similar) in the context of a file or folder discussed in the conversation, always:
1. Use `osascript -e 'tell application "Finder" to select POSIX file "/absolute/path"'` to reveal and select it
2. Never open the file — just select it in its directory
3. Do this via Bash, as efficiently as possible (no extra explanation needed)

**Why:** User prefers quick Finder navigation without accidentally opening files.
**How to apply:** Any time a file/folder path is known from context and user says "show me", "show", "where is it", "take me to it", or similar navigation intent.
