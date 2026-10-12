# Kona 3D prints

3D-printed organisers for the centre console of a 2025 Hyundai Kona, designed with Claude and printed on a Bambu Lab printer.

| Where | What | Current |
|---|---|---|
| [`rear-tray/`](rear-tray) | Tray for the bin under the armrest: two snap-in lip balm cradles, key fob pocket, one big bay; tapered to wedge in the bin | v11 (`rear-v11`) |
| [`front-tray/`](front-tray) | Narrow tray for the strip between the cupholders and the drive-mode panel: locating tongue, lip balm cradle, key fob pocket | v1 (`front-v1`), strip width still to be measured |
| [`reference/photos/`](reference/photos) | Photos and marked-up previews sent during the design conversations | |
| [`docs/conversations/`](docs/conversations) | Records of the design conversations, and their messages word for word in `raw/` | |
| [`docs/decisions.md`](docs/decisions.md) | Decision log | |

Each part folder has the CadQuery script, the render script, STL, 3MF and STEP files, a 3D preview, a dimensioned top view and a README with print settings and the numbers to change for fit.

Every delivered version is one commit, dated when it was sent, with a message starting `rear: vN` or `front: vN`. To get an old version: `git checkout rear-v4 -- rear-tray` once the tags exist (run `tools/tag-versions.sh` once from your own checkout; Claude's sessions can't push tags), or find the commit with `git log --oneline`. Rear v1 to v10 were rebuilt after the fact from the design session; see [the rear tray record](docs/conversations/2026-09-27-rear-console-tray.md#how-this-history-was-rebuilt).

## Rebuilding a part
```
pip install cadquery trimesh numpy-stl matplotlib
cd rear-tray && python3 kona_organiser.py && python3 render.py && python3 dims.py
cd front-tray && python3 kona_front_organiser.py && python3 render_front.py
```
