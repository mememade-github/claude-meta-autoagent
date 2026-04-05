# mdstat — Sample Project

A simple Markdown document statistics CLI tool. This sample demonstrates the `/refine` autonomous improvement loop.

## Try it

```bash
# Analyze a file
python app.py README.md

# JSON output
python app.py --json README.md

# Pipe from stdin
echo "# Hello World" | python app.py -
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

## Intentional gaps

This sample is deliberately imperfect — it provides room for the agent to improve:
- No handling of malformed markdown
- Limited error messages
- Missing features (e.g., table counting, image counting)
- No performance optimization for very large files

These are the kinds of gaps that `/refine` discovers and fixes autonomously.
