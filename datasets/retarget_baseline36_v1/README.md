# `retarget_baseline36_v1` freeze checklist

This directory is a schema/checklist placeholder, not a claim that the 36-image formal
dataset exists. Before the first formal four-method run, provide an audited immutable
manifest with exactly 36 real sources and two non-trivial target ratios per source.

Required source fields are the same as `retarget_smoke_real_v1`: stable source ID,
relative image path, dimensions, SHA-256, split, scene profile, source kind, license
status and scene category. A separate source-audit CSV must record official source,
license, access date, hash, local filename, redistribution status, author, attribution
and rights boundary. Images remain in `local_data/retarget_baseline36_v1/` and must not
be committed.

Freeze gates:

1. exactly 36 enabled sources and 72 enabled tasks;
2. source hashes and decoded dimensions match the audit table;
3. no unknown or unclear license or redistribution status;
4. target pressure is non-trivial and fixed before generation;
5. dataset fingerprint is recorded in Grill C;
6. run ID is new and output directory does not already contain another configuration;
7. a human has completed real Smoke A/B/C/Skip review and the scoring rubric is frozen.

After these gates pass:

```powershell
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_baseline36_v1
.\.venv\Scripts\retarget-agent.exe run generate configs\baseline36.example.yaml
```
