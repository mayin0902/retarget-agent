# Held-out240 Codex visual review

Date: 2026-08-12
Run: `square-public-v2-heldout240-20260812`
Evaluation: `auto-proxy-v1p1-heldout240-20260812`

## Scope and method

This is a purposive, non-blind Codex review of 14 real-world held-out tasks. For
each of the seven scene categories, the sample includes (a) the task with the
lowest score among its four candidates and (b) the task with the largest
between-method proxy-score spread. The source and all four frozen 1024-square
candidates were viewed together at high detail.

This review is diagnostic evidence, not a replacement for randomized human
A/B/C calibration. It deliberately over-samples hard cases and therefore must
not be reported as a 14-task success rate or extrapolated to all 240 tasks.

## Findings

| Scene | Selection | Task | Automatic evidence | Codex visual finding |
|---|---|---|---|---|
| Chinese dense poster | lowest best score | `commons-820ff9b73ba3__square-1024x1024` | best 63.21; spread 4.79 | No candidate is clean. Crop removes surrounding context and lower material; the other methods keep more text but compress the poster and illustrations. |
| Chinese dense poster | largest spread | `commons-c968ebe8802f__square-1024x1024` | best 83.04; spread 30.26 | Crop keeps the illuminated Chinese banner legible but discards much of the street context. Direct/seam preserve the scene with horizontal compression; mesh is visibly over-compressed. |
| Complex mixed | lowest best score | `commons-94832ce9dc9c__square-1024x1024` | best 61.12; spread 5.64 | The dense brochure remains recognizable, but small text is not reliably readable. Crop deletes most panels; full-content methods squeeze the complete layout. |
| Complex mixed | largest spread | `commons-ef08224d83be__square-1024x1024` | best 91.10; spread 28.77 | Direct warp retains the vendor, cart, and surrounding scene and is the most understandable relaxed-criterion result. Mesh visibly distorts the face and cart; crop loses left-side context. |
| Structure / architecture | lowest best score | `commons-53d86ead4d3d__square-1024x1024` | best 54.28; spread 4.88 | No strong result. Crop removes much of the shipyard; the other methods compress the scaffolding, people, and hull geometry. |
| Structure / architecture | largest spread | `commons-13481c146cfa__square-1024x1024` | best 91.81; spread 31.40 | Crop produces the most natural bridge composition but omits substantial left/right content. Full-content methods retain coverage at the cost of obvious geometry compression. |
| Multi-person | lowest best score | `commons-1296f31d179c__square-1024x1024` | best 52.14; spread 6.79 | Crop removes most of the team. Direct, seam, and mesh retain the lineup but compress bodies; none meets a strict no-deformation criterion. |
| Multi-person | largest spread | `oi-0047534bb816eb48__square-1024x1024` | best 83.10; spread 36.59 | The scene remains understandable in direct/crop/seam. Mesh introduces conspicuous structure and person deformation, consistent with its low proxy score. |
| Multi-product commercial | lowest best score | `commons-8409bac07d6a__square-1024x1024` | best 54.37; spread 11.40 | Crop reduces a multi-coin comparison to partial coins. Full-content methods preserve more items but distort their circular shape; no candidate is strong. |
| Multi-product commercial | largest spread | `oi-031244297d177089__square-1024x1024` | best 83.47; spread 24.45 | Direct keeps both labelled bottles but visibly changes bottle proportions. Crop loses product and label areas. The high direct score is too generous under a strict product-shape criterion. |
| Portrait | lowest best score | `commons-35a2ab968e9a__square-1024x1024` | best 47.83; spread 5.57 | Crop removes the face and lower body. Full-content methods keep the person but widen the body; none is a strict pass. |
| Portrait | largest spread | `commons-c2ecf47fc53e__square-1024x1024` | crop 85.04; spread 37.89 | Crop keeps face/torso geometry but amputates the lower-body pose. The proxy ranking is misaligned with whole-subject preservation here; full-content methods are complete but too wide. |
| Single product promo | lowest best score | `commons-83c3e3a85ed1__square-1024x1024` | best 55.01; spread 10.95 | Crop loses the carriage and much of the advertisement copy. Full-content methods retain the ad but squeeze typography and product geometry. |
| Single product promo | largest spread | `oi-07c9baa2741e5b90__square-1024x1024` | best 77.76; spread 33.09 | Direct/seam/mesh keep the recognizable food subject; crop removes much of the bowl. The very large score spread appears partly detector-driven rather than a similarly large perceived-quality difference. |

## Consequences for interpretation

- The automatic proxy is useful for routing and detects many severe crop/mesh
  failures, but it is not calibrated perceptual quality.
- Whole-subject completeness needs more weight for portraits, products, and
  lineups. A crop with a clean face or label can still be unacceptable when it
  removes the body, product, or surrounding message.
- Direct warp is often the strongest relaxed-criterion fallback because it
  preserves all information, but its score can under-penalize aspect distortion.
- The benchmark must report proxy quality, route regret, detector preservation,
  and this visual limitation together. It must not call proxy A/B a human pass.

The temporary seven contact sheets used for this review are stored under the
Git-ignored `local_data/heldout240_codex_review/` directory. The immutable Run
visualizations remain the source of truth.
