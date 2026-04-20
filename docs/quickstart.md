# Quick Start Guide

Two usage levels, from simplest to full Meta-Evolution.

---

## Level 1: Add /refine to an external project (no meta-evolution)

Copy the agent system for standalone /refine only. This does **not** create a sub-project — for the full 2-layer ROOT→Sub-project architecture, see Level 2.

```bash
# Clone this repo
git clone https://github.com/mememade-github/claude-meta-autoagent.git

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

## Level 2: Full 2-layer Meta-Evolution

The complete system: ROOT agent observes a sub-project agent and evolves the agent system itself.

### Step 1: Start the ROOT container

Open this repo in VS Code → "Reopen in Container", or:
```bash
cd .devcontainer
docker compose up -d
```

### Step 2: Start the sub-project container

```bash
cd projects/<sub-project>/.devcontainer
docker compose up -d
```

Now you have two containers: `claude-meta-autoagent` (ROOT) and `<sub-project>` (sub-project).

### Step 3: Authenticate Claude Code in the sub-project container

The sub-project container needs Claude Code authentication to run headless agents.

**Option A: API key** (recommended for headless agents):
```bash
# Set your API key in the sub-project's .env
echo "ANTHROPIC_API_KEY=your-key-here" >> projects/<sub-project>/.devcontainer/.env

# Restart the container to pick up the key
cd projects/<sub-project>/.devcontainer && docker compose up -d
```

**Option B: Interactive login** (for manual testing):
```bash
docker exec -it <sub-project> claude login
```

### Step 4: Launch a headless agent in the sub-project

From the ROOT container:
```bash
docker exec -d <sub-project> bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality of the app" \
   > /tmp/agent.log 2>&1'
```

### Step 5: Observe from ROOT

```bash
# Is the agent running?
docker exec <sub-project> ps aux | grep claude

# Check agent log
docker exec <sub-project> cat /tmp/agent.log

# Check refinement status
docker exec <sub-project> cat /workspaces/.refine-output 2>/dev/null

# Check git commits
docker exec <sub-project> git -C /workspaces log --oneline -5

# Check cross-run learning data
docker exec <sub-project> ls /workspaces/.claude/agent-memory/skills/ 2>/dev/null
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
./scripts/sync/sync-claude.sh projects/<sub-project>

# 3. Restart sub-project agent with the improved system
docker exec <sub-project> pkill -f claude  # stop old agent
docker exec -d <sub-project> bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality" \
   > /tmp/agent.log 2>&1'

# 4. Observe again — did the improvement help?
```

---

## Adding your own sub-project

Sub-projects are **internal to the ROOT system** — they live inside `projects/*/`, receive `.claude/` via sync, and are observed by ROOT for meta-evolution.

```bash
# 1. Create project directory structure
mkdir -p projects/my-project/.claude/{agents,hooks,skills,rules/project}
mkdir -p projects/my-project/.devcontainer
mkdir -p projects/my-project/.refine

# 2. Sync agent system from ROOT (makes this a sub-project)
./scripts/sync/sync-claude.sh projects/my-project

# 3. Copy DevContainer template (from ROOT .devcontainer; then edit
#    docker-compose.yml for a unique container_name and offset ports)
cp .devcontainer/Dockerfile projects/my-project/.devcontainer/
cp .devcontainer/entrypoint.sh projects/my-project/.devcontainer/
cp .devcontainer/setup-env.sh projects/my-project/.devcontainer/
cp .devcontainer/docker-compose.yml projects/my-project/.devcontainer/
cp .devcontainer/devcontainer.json projects/my-project/.devcontainer/

# 4. Set UNIQUE container name and ports (REQUIRED — avoids collision)
cat > projects/my-project/.devcontainer/.env << 'EOF'
CONTAINER_NAME=my-project
PORT_APP=5000
PORT_API=5080
HOST_WORKSPACE_PATH=
EOF

# 5. Create CLAUDE.md (sections 1-5 from ROOT, NO section 6 Meta-Evolution)
#    Sub-projects are the target of meta-evolution, not the subject.
#    Start from ROOT CLAUDE.md, strip §6, edit Identity section to match your project.

# 6. Create your scorer (.refine/score.sh)
#    Must output: SCORE: 0.XX and GAPS: [ID1, ID2, ...]

# 7. Create .gitignore for runtime artifacts (e.g., .refine-output, __pycache__, etc.)

# 8. Track in ROOT repo (optional — or add to .gitignore exceptions)
#    To include in public repo: add !projects/my-project/ to ROOT .gitignore
#    To keep private: projects/*/ pattern already gitignores it

# 9. Start container, run headless agent, observe from ROOT
cd projects/my-project/.devcontainer && docker compose up -d
docker exec -d my-project bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality" \
   > /tmp/agent.log 2>&1'
```
