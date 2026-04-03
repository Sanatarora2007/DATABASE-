---
name: Always use iMCP for weather, include it for location/travel/outdoor queries
description: iMCP is the primary weather source; always reference it when Sanat asks about travel, directions, or outdoor activities
type: feedback
---

Always use iMCP weather tools (`mcp__iMCP__weather_*`) for all weather-related queries.

**Why:** Sanat explicitly set iMCP as the preferred weather source.

**How to apply:**
- Any direct weather question → use iMCP weather tools
- Any query involving travel to a location, directions, ETA, or outdoor activity → proactively pull weather from iMCP and include it in the response alongside the maps/directions info
- Tools available: `weather_current`, `weather_hourly`, `weather_daily`, `weather_minute`
