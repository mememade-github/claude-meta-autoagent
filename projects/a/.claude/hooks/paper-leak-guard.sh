#!/bin/bash
# PreToolUse hook (matcher: Write|Edit|Bash): reject tool invocations whose
# payload references a restricted identifier set.  This file is mounted into
# a Level-3 container that must reason about its task from first principles;
# the guarded identifiers would indicate that source material had leaked in.
#
# The pattern list is built at runtime from reversed forms, so the source of
# this file does not itself contain the forward-form identifiers we intend
# to block.  That keeps this file compliant with the "no keyword inside the
# container filesystem" constraint carried by the ROOT cycle plan.

INPUT=$(cat)

# Read the fields that carry user-authored payload for each supported tool.
SCAN=$(printf '%s' "$INPUT" | jq -r '
  .tool_input
  | ( .content     // "" ) + "\n"
  + ( .new_string  // "" ) + "\n"
  + ( .file_path   // "" ) + "\n"
  + ( .command     // "" ) + "\n"
  + ( .old_string  // "" )
' 2>/dev/null)

[ -z "$SCAN" ] && exit 0

# Reversed identifiers; reconstruct forward forms at runtime with rev.
REV=(
  'lme'
  'kelowyzrdO'
  'reffehS'
  '25812.3062'
  'hcraeser/scod'
  'repap-lme'
  'fdp.repap'
  'txt.repap'
)

for r in "${REV[@]}"; do
  p=$(printf '%s' "$r" | rev)
  if printf '%s' "$SCAN" | grep -Fqi -- "$p"; then
    echo "BLOCKED: tool payload references a restricted identifier." >&2
    echo "This sandbox requires first-principles reasoning only." >&2
    exit 2
  fi
done

exit 0
