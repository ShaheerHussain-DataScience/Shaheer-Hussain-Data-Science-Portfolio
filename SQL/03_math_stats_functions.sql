
-- ============================================================================
-- MATH & STATISTICS HELPERS
-- Safe division, median, percentiles, MAD, rolling helpers on arrays.
-- ============================================================================
SET search_path = public;

-- safe_divide(numerator numeric, denominator numeric, fallback numeric) -> numeric
-- Example: SELECT safe_divide(10, 0, NULL); -- NULL
CREATE OR REPLACE FUNCTION safe_divide(numerator NUMERIC, denominator NUMERIC, fallback NUMERIC DEFAULT NULL)
RETURNS NUMERIC LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE WHEN denominator = 0 THEN fallback ELSE numerator / denominator END;
$$;

-- median_samp(anyarray) -> numeric
-- Median from a numeric array. NULL for empty arrays.
-- Example: SELECT median_samp(ARRAY[10,2,5,9]); -- 7.5
CREATE OR REPLACE FUNCTION median_samp(values NUMERIC[])
RETURNS NUMERIC LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE sorted NUMERIC[]; n INT; mid INT;
BEGIN
  IF values IS NULL OR array_length(values,1) IS NULL THEN RETURN NULL; END IF;
  sorted := (SELECT array_agg(v ORDER BY v) FROM unnest(values) v);
  n := array_length(sorted,1);
  mid := (n+1)/2;
  IF n % 2 = 1 THEN
    RETURN sorted[mid];
  ELSE
    RETURN (sorted[mid] + sorted[mid+1]) / 2.0;
  END IF;
END; $$;

-- percentile_samp(values numeric[], p numeric between 0 and 1) -> numeric
-- Example: SELECT percentile_samp(ARRAY[1,2,3,4,5], 0.9); -- 4.6 by linear interpolation
CREATE OR REPLACE FUNCTION percentile_samp(values NUMERIC[], p NUMERIC)
RETURNS NUMERIC LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE arr NUMERIC[]; n INT; pos NUMERIC; lower INT; upper INT; frac NUMERIC;
BEGIN
  IF values IS NULL OR array_length(values,1) IS NULL OR p IS NULL THEN RETURN NULL; END IF;
  IF p < 0 OR p > 1 THEN RAISE EXCEPTION 'p must be between 0 and 1'; END IF;
  arr := (SELECT array_agg(v ORDER BY v) FROM unnest(values) v);
  n := array_length(arr,1);
  IF n = 1 THEN RETURN arr[1]; END IF;
  pos := (n - 1) * p + 1;
  lower := floor(pos)::int;
  upper := ceil(pos)::int;
  frac := pos - lower;
  IF upper > n THEN upper := n; END IF;
  RETURN arr[lower] + frac * (arr[upper] - arr[lower]);
END; $$;

-- mad_zscore(values numeric[], scale numeric default 1.4826) -> numeric[]
-- Returns array of robust z-scores (deviation from median scaled by MAD).
-- Example:
--   SELECT mad_zscore(ARRAY[10,11,9,50,10]); -- large value near 50
CREATE OR REPLACE FUNCTION mad_zscore(values NUMERIC[], scale NUMERIC DEFAULT 1.4826)
RETURNS NUMERIC[] LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE med NUMERIC; mad NUMERIC; res NUMERIC[] := '{}';
BEGIN
  IF values IS NULL OR array_length(values,1) IS NULL THEN RETURN NULL; END IF;
  med := median_samp(values);
  mad := median_samp(ARRAY(SELECT abs(v - med) FROM unnest(values) v));
  IF mad = 0 THEN
    RETURN ARRAY(SELECT 0::numeric FROM unnest(values));
  END IF;
  RETURN ARRAY(SELECT (v - med) / (scale * mad) FROM unnest(values) v);
END; $$;

-- cagr(initial numeric, final numeric, years numeric) -> numeric
-- Compound Annual Growth Rate as a decimal (e.g., 0.12 = 12%).
-- Example: SELECT cagr(100, 160, 3); -- ~0.1699
CREATE OR REPLACE FUNCTION cagr(initial NUMERIC, final NUMERIC, years NUMERIC)
RETURNS NUMERIC LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE WHEN initial <= 0 OR years <= 0 THEN NULL ELSE power(final / initial, 1/years) - 1 END;
$$;
