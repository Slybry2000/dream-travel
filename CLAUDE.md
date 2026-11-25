# Dream-Travel: rules to keep this folder caught up and clean

This repo is PUBLIC and auto-deploys to the live Dream Travel websites from `main`. Treat every commit as published.

## Start of any session
1. A check runs automatically (`.claude/catchup-check.sh`). If it says the branch is behind or dirty, fix that FIRST.
2. Start new work from a fresh branch off the live site: `git fetch origin` then `git switch -c <short-name> origin/main`.
   Never keep building on an old feature branch. `origin` is HTTPS now, so `git fetch` works (SSH has no key on this PC).

## While working
3. One task = one short branch = merged to `main` and deleted within a few days. Do not leave long-lived feature branches.
4. Commit finished work at the end of the session. Never leave edits uncommitted overnight (that is how 90 dirty files piled up).
5. Check before you commit: `git status`. Only site files belong here. Big working folders (flyers, decks, lead lists, intake tools, tmp) live outside the repo or in the local ignore list (`.git/info/exclude`); never `git add -f` them.
6. Commit only your own paths. Other Claude sessions edit this repo; never commit someone else's uncommitted changes.
7. Client-named trips (`status: draft` in `_trips/data/*.json`) are NEVER committed. The pre-commit guard blocks them, files over 3 MB, working folders and `.bak` files.
8. Generated pages (`trips/library-*`): rebuild with `python _trips/build.py` from an up-to-date branch, then commit the output. Never hand-edit them, and never keep a stale rebuild around: it conflicts with main.

## End of session
9. Merge or open a PR for finished work; delete the branch after it merges (`git branch -d <name>`).
10. Remove agent worktrees (`git worktree remove <path>`) when their branch is merged. Do not leave old `.claude/worktrees/*`.
11. Pushing to `main` publishes to the live site: ask Bryan first unless he said to publish. Push over HTTPS.
