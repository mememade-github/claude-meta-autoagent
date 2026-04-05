# Quick Start Guide

Three usage levels, from simplest to full Meta-Evolution.

---

## Level 1: Add /refine to your existing project

Copy the agent system and start improving your project immediately.

```bash
# Clone this repo
git clone https://github.com/mememade/claude-meta-autoagent.git

# Copy .claude/ to your project
cp -r claude-meta-autoagent/.claude/ /path/to/your/project/.claude/
cp claude-meta-autoagent/CLAUDE.md /path/to/your/project/CLAUDE.md
```

Create a scorer at `.refine/score.sh` in your project:
```bash
#!/bin/bash
PASS=0; TOTAL=0; GAPS=()

check() {
  local id="$1"; shift; shift
  TOTAL=$((TOTAL + 1))
  if eval "$@" > /dev/null 2>&1; then PASS=$((PASS + 1)); else GAPS+=("$id"); fi
}

# Your checks here
check "T1" "Tests pass" 'python -m pytest tests/'
check "B1" "Build succeeds" 'npm run build'

SCORE=$(echo "$PASS $TOTAL" | awk '{printf "%.2f", $1/$2}')
GAP_STR=$(printf ", %s" "${GAPS[@]}")
echo "SCORE: $SCORE"
echo "GAPS: [${GAP_STR:2}]"
```

Then in Claude Code:
```
/refine "improve production quality"
```

---

## Level 2: Try the sample project

Experience `/refine` with the included sample app.

```bash
cd projects/sample-app

# Run the app
echo "# Hello World" | python3 app.py -

# See current quality score
bash .refine/score.sh

# In Claude Code, run /refine
/refine "improve the sample app" --project ./projects/sample-app
```

The agent discovers gaps (error handling, edge cases), fixes them one at a time, and iterates.

---

## Level 3: Full 2-layer Meta-Evolution

The complete system: ROOT agent observes a sub-project agent and evolves the agent system itself.

### Step 1: Start the ROOT container

Open this repo in VS Code → "Reopen in Container", or:
```bash
cd .devcontainer
docker compose up -d
```

### Step 2: Start the sub-project container

```bash
cd projects/sample-app/.devcontainer
docker compose up -d
```

Now you have two containers: `claude-meta-autoagent` (ROOT) and `sample-app` (sub-project).

### Step 3: Authenticate Claude Code in the sub-project container

The sub-project container needs Claude Code authentication to run headless agents.

**Option A: API key** (recommended for headless agents):
```bash
# Set your API key in the sub-project's .env
echo "ANTHROPIC_API_KEY=your-key-here" >> projects/sample-app/.devcontainer/.env

# Restart the container to pick up the key
cd projects/sample-app/.devcontainer && docker compose up -d
```

**Option B: Interactive login** (for manual testing):
```bash
docker exec -it sample-app claude login
```

### Step 4: Launch a headless agent in the sub-project

From the ROOT container:
```bash
docker exec -d sample-app bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality of the app" \
   > /tmp/agent.log 2>&1'
```

### Step 5: Observe from ROOT

```bash
# Is the agent running?
docker exec sample-app ps aux | grep claude

# Check agent log
docker exec sample-app cat /tmp/agent.log

# Check refinement status
docker exec sample-app cat /workspaces/.refine-output 2>/dev/null

# Check git commits
docker exec sample-app git -C /workspaces log --oneline -5

# Check cross-run learning data
docker exec sample-app ls /workspaces/.claude/agent-memory/skills/ 2>/dev/null
```

### Step 6: Diagnose — project issue or system issue?

The key question: is the problem in the **project code** or the **agent system**?

| Observation | Diagnosis | Who fixes |
|-------------|-----------|-----------|
| Agent stuck in loop | System: SKILL.md termination logic | **You (ROOT)** — fix `.claude/skills/refine/SKILL.md` |
| Agent modifies scorer + code together | System: scorer independence rule too weak | **You (ROOT)** — strengthen CLAUDE.md §2 |
| Agent doesn't use past failures | System: cross-run learning integration gap | **You (ROOT)** — fix Audit step in SKILL.md |
| Agent tries wrong approach for this project | Project: scorer doesn't penalize it | **Sub-project agent** — leave it, scorer will evolve |
| Code has bugs after /refine | Project: test coverage gap | **Sub-project agent** — scorer needs more checks |

**ROOT evolves the system. Sub-project agent evolves the implementation.**

### Step 7: Meta-Evolution cycle — fix system, sync, re-observe

```bash
# 1. Fix .claude/ files in ROOT (the META evolution)
#    Example: improve SKILL.md to prevent the pattern you observed

# 2. Sync the improved system to sub-project
./scripts/sync/sync-claude.sh projects/sample-app

# 3. Restart sub-project agent with the improved system
docker exec sample-app pkill -f claude  # stop old agent
docker exec -d sample-app bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality" \
   > /tmp/agent.log 2>&1'

# 4. Observe again — did the improvement help?
```

---

## Adding your own sub-project

```bash
# Create project directory
mkdir -p projects/my-project/.claude/{agents,hooks,skills,rules/project}
mkdir -p projects/my-project/.devcontainer
mkdir -p projects/my-project/.refine

# Sync agent system from ROOT
./scripts/sync/sync-claude.sh projects/my-project

# Copy DevContainer template
cp .devcontainer/Dockerfile projects/my-project/.devcontainer/
cp .devcontainer/entrypoint.sh projects/my-project/.devcontainer/
cp .devcontainer/setup-env.sh projects/my-project/.devcontainer/
cp projects/sample-app/.devcontainer/docker-compose.yml projects/my-project/.devcontainer/
cp projects/sample-app/.devcontainer/devcontainer.json projects/my-project/.devcontainer/

# Edit .env with unique container name and ports
cat > projects/my-project/.devcontainer/.env << 'EOF'
CONTAINER_NAME=my-project
PORT_APP=5000
PORT_API=5080
HOST_WORKSPACE_PATH=
EOF

# Create your scorer and CLAUDE.md
# Then: docker compose up, run headless agent, observe
```
