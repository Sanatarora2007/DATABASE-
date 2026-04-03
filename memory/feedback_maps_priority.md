---
name: Always use Google Maps as primary, Apple Maps as fallback
description: Google Maps (mcp__google-maps__*) is primary for all maps/location tasks; Apple Maps (iMCP) only as fallback
type: feedback
---

Always use Google Maps MCP (`mcp__google-maps__*`) as the primary tool for maps, directions, geocoding, and location lookups.

**Why:** Apple Maps is inaccurate in India. Google Maps gives much better results.

**How to apply:** 
- For location lookup: get coordinates via `mcp__iMCP__location_current`, then reverse geocode via `mcp__google-maps__maps_reverse_geocode`
- For directions, place search, ETA: use `mcp__google-maps__*` tools first
- Only fall back to iMCP maps tools (`mcp__iMCP__maps_*`) if Google Maps API fails or quota runs out
