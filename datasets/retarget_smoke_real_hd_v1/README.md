# retarget_smoke_real_hd_v1

This is the high-resolution successor to `retarget_smoke_real_v1`. It preserves
the same twelve audited real-world scenes and exact 2/2/2/2/1/1/2 category
stratification, while using the official original or largest practical
Wikimedia rendition recorded in `source_manifest.csv`.

The new target catalog is 1024×1024, 1536×800, and 864×1536. Each source is
assigned the two most different non-trivial aspect ratios. Candidate PNGs are
therefore generated at reviewable HD dimensions instead of the old 216–384 px
preview dimensions.

The 1940 `Meng Lijun` poster has only a 310×450 public original. Its HD
candidate files have HD canvas dimensions but cannot contain detail absent from
the source; reviewers should judge preservation/composition and record source
resolution limits rather than interpreting interpolation as recovered detail.

Materialize with:

```powershell
.\.venv\Scripts\python.exe scripts\materialize_real_smoke_hd.py
```

Image bytes remain under the Git-ignored `local_data/` tree. Git stores this
manifest, the materializer, and the audit/readme only.
