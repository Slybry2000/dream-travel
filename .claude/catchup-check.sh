#!/bin/sh
# Runs at the start of every Claude session in this repo. Prints a warning only if something is off.
cd "$(dirname "$0")/.." || exit 0
git fetch origin --quiet 2>/dev/null || echo "WARNING: could not reach GitHub (fetch failed); behind-main check is unreliable."
br=$(git branch --show-current)
behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")
dirty=$(git status --porcelain | wc -l | tr -d ' ')
msg=""
[ "$behind" != "0" ] && msg="$msg\n- This branch ($br) is $behind commits BEHIND the live site (origin/main). Start new work from a fresh branch off origin/main."
[ "$dirty" != "0" ] && msg="$msg\n- $dirty uncommitted changes are sitting here. Commit them to a branch or discard them before starting something new."
[ "$br" = "main" ] && msg="$msg\n- You are ON main. Make a branch (git switch -c <name>) before editing."
if [ -n "$msg" ]; then printf "DREAM-TRAVEL CATCH-UP CHECK:$msg\nRules: see CLAUDE.md in this folder.\n"; else echo "Dream-Travel: caught up with the live site and clean."; fi
exit 0
