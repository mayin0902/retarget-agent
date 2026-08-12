# retarget_smoke_real_square_v1

This is the complete 1:1 Round 0 benchmark. It reuses all twelve independently
audited public real-world sources from `retarget_smoke_real_hd_v1`, with exactly
one 1536x1536 task per source. The fixed scene distribution remains
2/2/2/2/1/1/2 across Chinese posters, single products, mixed commerce,
multi-person, portrait, structure, and difficult mixed scenes.

The source license and attribution evidence remains in
`datasets/retarget_smoke_real_hd_v1/source_manifest.csv`. Image bytes and
materialized CSV files remain under the Git-ignored `local_data/` directory.

Materialize and validate with:

```powershell
.\.venv\Scripts\python.exe scripts\materialize_real_smoke_square.py
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_smoke_real_square_v1
```

All four traditional methods must finish all 12 tasks (48 candidates) before
this round is ranked. The dataset is a technical pilot, not the final 300-image
public benchmark and not human-scored ground truth.
