#!/bin/bash
set -e

echo "=== Setting up Claude Code ==="

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Create .claude directory structure
mkdir -p ~/.claude/projects

# Symlink skills
ln -sf "$(pwd)/.claude/skills" ~/.claude/skills

# Symlink plugins
ln -sf "$(pwd)/.claude/plugins" ~/.claude/plugins

# Symlink settings
ln -sf "$(pwd)/.claude/settings.json" ~/.claude/settings.json

# Symlink MCP configs
ln -sf "$(pwd)/.claude/.mcp.json" ~/.claude/.mcp.json
ln -sf "$(pwd)/mcp.json" ~/.claude/mcp.json

# Copy CLAUDE.md to home (global)
cp "$(pwd)/CLAUDE.md" ~/CLAUDE.md

# Symlink memory to project directory
PROJ_DIR=~/.claude/projects/-home-codespace-DATABASE-
mkdir -p "$PROJ_DIR"
ln -sf "$(pwd)/memory" "$PROJ_DIR/memory"

echo ""
echo "=== Claude Code Setup Complete ==="
echo "Skills:  $(ls .claude/skills | wc -l) skills linked"
echo "Memory:  $(ls memory | wc -l) memory files linked"
echo "Plugins: linked"
echo "MCPs:    linked"
echo ""
echo "Run 'claude' to start Claude Code"
echo ""
echo "NOTE: Gmail, Google Calendar, Google Maps, Canva work directly."
echo "For WhatsApp, Apple Events, Apple Mail — your Mac must be running"
echo "with Tailscale tunnel active."
