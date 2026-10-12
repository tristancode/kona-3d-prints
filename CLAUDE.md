# Working in this repo

- Each part has one folder holding its current version: `rear-tray/`, `front-tray/`. Older versions are in git history as commits named `rear: vN - ...` / `front: vN - ...`, tagged `rear-vN` / `front-vN` by `tools/tag-versions.sh` (cloud sessions cannot push tags).
- Geometry comes from the part's CadQuery script; print files (STL, 3MF, STEP) and pictures are outputs. Change the numbers at the top of the script, re-run it, then re-run the render script. Never edit an output by hand.
- Every render includes measurements on each edge (the dimensioned top view).
- One commit per delivered version, message `<part>: vN - <what changed>`; version numbers never repeat.
- At the end of each working session, update that conversation's record in `docs/conversations/` (and its messages in `raw/`), add any decisions to `docs/decisions.md`, and commit them with the files produced.
- Tools: `pip install cadquery trimesh numpy-stl matplotlib`.
