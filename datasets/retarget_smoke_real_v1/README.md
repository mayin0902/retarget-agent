# retarget_smoke_real_v1

This directory versions only the audited source manifest and documentation. Image bytes are downloaded into Git-ignored `local_data/retarget_smoke_real_v1/`.

Materialize and validate on Windows:

```powershell
.\.venv\Scripts\python.exe scripts\materialize_real_smoke.py
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_smoke_real_v1
```

The script accepts only versioned HTTPS URLs on approved official hosts, verifies SHA-256 and dimensions, rejects unclear redistribution status, checks the required 12-image scene distribution, and chooses the two target ratios farthest from each source aspect ratio. It never downloads a complete upstream dataset.

