---
name: chrome-connect
description: "Ensure Chrome is open and the extension is connected before doing browser automation. Trigger on: '/chrome-connect', 'open chrome', 'chrome not working', 'browser not connected', or automatically when mcp__claude-in-chrome tools fail with 'No Chrome extension connected'."
---

# Chrome Connect

When Claude in Chrome is not working or returns "No Chrome extension connected":

1. Check if Chrome is running:
   - Run `pgrep -x "Google Chrome"` 
   - If no output → Chrome is not open

2. If Chrome is not open:
   - Run `open -a "Google Chrome"`
   - Wait a moment for it to launch
   - Tell the user: "Chrome was not open — launching it now. Make sure the Claude Code Chrome extension is enabled, then I'll retry."

3. If Chrome is already open:
   - Tell the user: "Chrome is open but the extension isn't connected. Make sure the Claude Code Chrome extension is active in Chrome (check the extensions bar)."

4. After Chrome is confirmed open, retry the original browser task using `mcp__claude-in-chrome__tabs_context_mcp` with `createIfEmpty: true`.

5. If it still fails after Chrome is open, tell the user: "Chrome is open but the extension still isn't responding. Try reloading the extension from chrome://extensions or restarting Chrome."
