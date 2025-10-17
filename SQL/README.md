# PostgreSQL Functions-Only Toolkit

Drop-in, commented functions for everyday analyst/scientist tasks.
Each function has a minimal, stable signature and examples in comments.
Dialect: **PostgreSQL 12+**.

## Files
- `01_text_utils_functions.sql` — text normalization, slugify, email & URL domain extraction, safe left-pad.
- `02_date_time_functions.sql` — month boundaries, N-minute bucketing, business-day counts, working minutes within hours.
- `03_math_stats_functions.sql` — safe divide, median/percentile from arrays, MAD-based z-scores, CAGR.
- `04_jsonb_functions.sql` — JSONB getters, deep merge, set value by path.
- `05_array_helpers.sql` — unique/compact/intersect/except for arrays.
- `06_analytics_shortcuts.sql` — money conversions, percent change, percentile labeler.

## Usage
1. Run any or all `.sql` files in your database (no schema assumptions; installed in `public` by default).
2. Call functions directly, e.g. `SELECT slugify('Hello World');`
3. Replace example literals in comments with your own values.

> If you prefer a custom schema (e.g., `utils`), prepend with:
> ```sql
> CREATE SCHEMA IF NOT EXISTS utils;
> SET search_path = utils, public;
> ```
