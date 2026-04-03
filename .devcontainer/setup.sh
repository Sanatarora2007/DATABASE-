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
echo "=== Setting up R2 database sync ==="

# Install boto3 for R2 access
pip3 install boto3 -q 2>/dev/null || pip3 install boto3 --break-system-packages -q 2>/dev/null

# R2 credentials — set as Codespace secrets or env vars
# In Codespace settings, add R2_ACCESS_KEY and R2_SECRET_KEY as secrets
REPO_DIR="$(pwd)"
if [ -n "$R2_ACCESS_KEY" ] && [ -n "$R2_SECRET_KEY" ]; then
    cat > ~/.r2-credentials << CREDS
access_key = $R2_ACCESS_KEY
secret_key = $R2_SECRET_KEY
CREDS
    chmod 600 ~/.r2-credentials
    echo "✓ R2 credentials configured from secrets"
else
    echo "⚠ Set R2_ACCESS_KEY and R2_SECRET_KEY as Codespace secrets for auto-sync"
fi

mkdir -p ~/synced-db

# Create refresh script using R2
cat > ~/refresh-db.sh << REFRESH
#!/bin/bash
cd "$REPO_DIR" 2>/dev/null || cd ~/DATABASE- 2>/dev/null
python3 db-sync/r2-download.py
REFRESH
chmod +x ~/refresh-db.sh

# Initial pull
bash ~/refresh-db.sh 2>/dev/null || echo "⚠ Initial DB pull failed — set R2 secrets"

# Auto-refresh every 30 seconds via cron
(crontab -l 2>/dev/null; echo "* * * * * bash ~/refresh-db.sh >> /tmp/db-refresh.log 2>&1") | sort -u | crontab -
(crontab -l 2>/dev/null; echo "* * * * * sleep 30 && bash ~/refresh-db.sh >> /tmp/db-refresh.log 2>&1") | sort -u | crontab -
sudo service cron start 2>/dev/null || true

echo "✓ R2 auto-refresh installed (every 30 seconds)"

echo ""
echo "=== Claude Code Setup Complete ==="
echo "Skills:  $(ls .claude/skills | wc -l) skills linked"
echo "Memory:  $(ls memory | wc -l) memory files linked"
echo "Plugins: linked"
echo "MCPs:    linked"
echo "DBs:     ~/synced-db/ (WhatsApp, Calendar, Reminders)"
echo ""
echo "Run 'claude' to start Claude Code"
echo "Run '~/refresh-db.sh' to pull latest database snapshots"
