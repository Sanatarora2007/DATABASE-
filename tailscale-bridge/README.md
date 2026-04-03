# Tailscale MCP Bridge

This bridges Mac-only MCPs (WhatsApp, Apple Events, Apple Mail, macOS Automator, Music) 
to Codespaces over Tailscale so they work from your iPhone.

## One-time Mac setup

1. Install Tailscale: `brew install tailscale`
2. Sign in: `tailscale login`
3. Start the MCP bridge server: `bash tailscale-bridge/start-bridge.sh`

## How it works

Your Mac runs a lightweight MCP proxy server on your Tailscale IP.
Codespaces connects to it via Tailscale, forwarding MCP calls to local Mac MCPs.

## Which MCPs need the bridge

| MCP | Needs bridge? | Why |
|-----|--------------|-----|
| WhatsApp | Yes | Chrome extension + local SQLite |
| Apple Events | Yes | macOS Calendar/Reminders |
| Apple Mail | Yes | macOS Mail.app |
| macOS Automator | Yes | AppleScript/osascript |
| Music | Yes | Apple Music on Mac |
| Gmail | No | OAuth cloud-based |
| Google Calendar | No | OAuth cloud-based |
| Google Maps | No | API cloud-based |
| Canva | No | OAuth cloud-based |
