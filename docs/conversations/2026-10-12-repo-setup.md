# Conversation record – repository set-up

| | |
|---|---|
| **Dates** | 2026-10-12 |
| **Area** | repo |
| **Claude project** | "Kona 3d print organiser", thread "Kona prints GitHub repo" (claude.ai, cloud session) |
| **People** | Charlimit, Claude |
| **Status** | Done |
| **Type** | Record (summary written by Claude, not a verbatim transcript) |

## Summary
Charlimit asked for a new repo, `kona-3d-prints`, with every version of every file committed so there is history, and conversation records kept the way the `pizza-oven` repo keeps them.

Claude read `pizza-oven` (attached read-only) for its layout, then deleted its copy once Charlimit asked for it to be disconnected. Charlimit created the empty private repo on GitHub (Claude may not create repositories). Claude built the history:

- One commit per delivered version, dated at the time it was sent in the conversation (Sydney time), tagged `rear-v1` … `rear-v11` and `front-v1`.
- The photos sent in the conversations, in `reference/photos/`, each committed with the version it led to.
- Rear v1 to v10 were rebuilt from the design session's transcript, and their print files and pictures regenerated (see the rear tray record). Rear v11 and front v1 are the original files.
- Conversation records in `docs/conversations/`, the visible messages word for word in `docs/conversations/raw/`, a decision log in `docs/decisions.md`, and `CLAUDE.md` with the working rules.

## Decisions

| Date | Decision |
|---|---|
| 2026-10-12 | One repo for all Kona prints; one folder per part holding the current version, older versions in git history under `<part>-vN` tags. |
| 2026-10-12 | Conversations are stored as records in `docs/conversations/` plus the visible messages in `raw/`, as in `pizza-oven`. |
| 2026-10-12 | Binary print files and photos are committed directly; Git LFS is not set up (about 40 MB in total). |
