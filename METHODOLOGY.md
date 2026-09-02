# Methodology: operational AnA versus USGS on the White River

Question: Does operational NWM analysis-assim beat yesterday's flow on the White River in 2025 to August 2026?

This tree is a new product. Frozen v2.1 science stays `fa2e315`. AnA RMSE does not enter that table. Live science `4fdedca`: AnA `t12z` `tm00` analysis beat persistence at all four gages (Nora 301 vs 1,179 yesterday). That does not reverse the v2.1 Anderson-only win. GraphForge pin `anaforge/` holds five refuse laws.

## Window

Calendar 2025-01-01 through 2026-08-31. 608 days. Files on 2026-09-01 exist and stay out. 2021-2024 AnA on AWS 404s and stays out.

## Layers

| Layer | Role | Source |
|-------|------|--------|
| Gages | Anderson 03348000, Nora 03351000, Indianapolis 03353000, Centerton 03354000 | NWIS daily 00060. Empty site stops. |
| COMID | NWM reach | 18474953, 18476353, 18476879, 18477453 (same as `fa2e315`) |
| AnA Q | analysis-assim streamflow | AWS `noaa-nwm-pds` `nwm.t12z.analysis_assim.channel_rt.tm00.conus.nc`, noon UTC, packed int × 0.01 m³/s to cfs. One missing day stops. |

Persistence is lag-1 00060 at that gage. No train. No Ridge. Residual is AnA minus USGS, in cfs.

## Skill

On days with finite USGS, AnA, and yesterday USGS: RMSE and MAE. AnA beats persistence when its RMSE is smaller.

## Figures

1. Nora hydrograph: USGS Q, persistence, AnA. Not feet.
2. Four-gage residual strip: mean (AnA minus USGS). Caption: not water.

## Claims

Allowed: AnA versus yesterday on this window; same four gages; fetch-or-stop per day; persistence is the bar; cite `fa2e315` as the frozen v2.1 parent.

Banned: mixing AnA and v2.1 RMSE in one table; interpolating a missing AnA day; 2021-2024 AnA fill; HAND as a FIRM; residual as inundation; flood warning; captioning tm00 analysis as a forecast; "NWM now wins."
