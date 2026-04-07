# Moltbook — Sample Project

A Moltbook AI social network integration demo. This sample demonstrates the `/refine` autonomous improvement loop.

## Try it

```bash
# Check agent status
python moltbook.py status

# Run the tests
python test_moltbook.py
```

## Run the scorer

```bash
bash .refine/score.sh
```

## Run /refine

From the ROOT workspace, with Claude Code:

```
/refine "improve the sample app" --project ./projects/sample-app
```

The agent will autonomously discover gaps via the scorer, fix them, and iterate until the score reaches the threshold.
