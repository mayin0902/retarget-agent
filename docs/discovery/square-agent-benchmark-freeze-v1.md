# 1:1 Agent benchmark freeze v1

> Frozen on 2026-08-12. This is an automatic, uncalibrated experiment track;
> it does not replace the blocked human-scored Grill C baseline.

## Completion rule

A benchmark arm is ranked only when it has one final output decision for every
task in that round. Partial arms are rejected by `retarget-agent benchmark
report`. A provider failure, budget rejection, invalid Agent JSON, or missing
generated candidate must fall back to a recorded traditional candidate so the
policy remains complete; it may not silently shrink the denominator.

The three rounds are:

| Round | Sources | Target | Traditional candidates | Purpose |
|---|---:|---:|---:|---|
| Round 0 | 12 audited real Smoke sources | 1536x1536 | 48 | End-to-end technical closure |
| Round 1 | 60 approved public pilot sources | 1024x1024 | 240 | Threshold/model/workflow selection |
| Round 2 | 240 held-out public sources | 1024x1024 | 960 | Frozen confirmatory comparison |

`full300` means the union of a completed `pilot60` and a completed
`held-out240`; it is never extrapolated from a partial run.

## Dataset strata

The final 300-source quota is 50/50/50/50/34/33/33 for Chinese dense poster,
single-product promotion, multi-product commercial, multi-person, portrait,
landscape/architecture/structure, and complex mixed scenes. The pilot60 quota
is 10/10/10/10/7/7/6.

Open Images official S3 validation copies were empirically measured at a
1024-pixel long edge. Therefore public benchmark v2 uses a native 1024x1024
evaluation canvas instead of upscaling those copies to claim 1536-source
detail. Aspect pressure remains 1.5--4.0. Wikimedia Commons and Open Images
pixels require per-image license, scene, safety, duplicate, and egress review.

## Complete policy arms

Each round reports:

1. all four fixed traditional methods: direct warp, crop, seam, and mesh;
2. the frozen no-Agent Generation selector;
3. the deterministic rules-only router;
4. conditional Qwen3-VL 4B, Qwen3-VL 8B, and SmolVLM2 2.2B routers;
5. always-on judge variants of the same three VLMs;
6. a proxy-metric Oracle used only as an automatic upper-reference, never as a
   deployable or human-gold method.

Always-on VLM inference is cached once per `(source hash, candidate hashes,
model revision, prompt/schema version)`. Conditional results are derived by
applying the frozen trigger mask to the same model responses; the model is not
called a second time. Thus Round 1 requires exactly 60 requests per VLM, 180
total, and Round 2 requires 240 per VLM, 720 total. Missing responses make that
model arm incomplete rather than changing its denominator.

## Generation budget and fairness

SeedDream is not an always-generate baseline. It is eligible only when a
controlled router marks all traditional candidates unreliable, the source row
has `api_egress_allowed=true`, and the hard budget accepts a reservation.

- one output at most per unique task;
- no automatic retry and no best-of-K;
- global experiment cap: 12 unique paid calls;
- reserve 0.60 CNY per call; expected range 0.30--0.60 CNY;
- worst-case reserved spend: 7.20 CNY;
- paid outputs are shared by every policy that selects the same task;
- actual provider cost remains null until billing evidence is available.

If more than 12 tasks request generation, a deterministic priority order
(multi-model agreement, then lowest traditional proxy score, then task ID)
selects the materialized set. Every non-materialized request falls back to its
best recorded traditional output, preserving a complete policy denominator.

The same materialized task set is used for raw SeedDream, SeedDream plus exact
text repaste, and the local AnyText2/text workflow. These workflow candidates
are scored at the common round canvas. Their policies include traditional
fallbacks for all other tasks and are therefore comparable over all 60/240
tasks rather than only the generated subset.

## Metrics

Quality reports proxy A/B success, mean quality score, OCR character recall,
face/person/product/logo preservation, visual integrity, content fidelity,
composition, structure lines, and transform safety. The current score is an
uncalibrated routing proxy: it is not a human ReviewGrade.

Efficiency reports candidate and end-to-end p50/p95 wall time, CPU seconds,
peak process RSS, Agent latency/tokens/JSON validity, remote GPU seconds and
peak VRAM when observable, and external-generation latency. Cost reports direct
provider spend separately from configurable infrastructure/energy estimates.
Unknown actual costs remain null, not zero. Routing reports call rate,
generation-request/fulfilment rate, top-1 change rate, proxy routing regret,
fallback rate, and complete task count.

The relaxed visual success interpretation for model/Codex review is: the main
subject and main message remain understandable, important text is not missing,
and there is no obvious subject, face, product, Logo, or structure deformation.
