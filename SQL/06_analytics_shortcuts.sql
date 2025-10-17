
-- ============================================================================
-- ANALYTICS SHORTCUTS
-- Common transformations you can drop into queries.
-- ============================================================================
SET search_path = public;

-- dollars_to_cents(numeric) -> bigint
-- Exact money-to-cents conversion avoiding floating errors.
-- Example: SELECT dollars_to_cents(19.99); -- 1999
CREATE OR REPLACE FUNCTION dollars_to_cents(amount NUMERIC)
RETURNS BIGINT LANGUAGE sql IMMUTABLE AS $$
  SELECT round(amount * 100)::bigint;
$$;

-- cents_to_dollars(bigint) -> numeric
-- Example: SELECT cents_to_dollars(1999); -- 19.99
CREATE OR REPLACE FUNCTION cents_to_dollars(cents BIGINT)
RETURNS NUMERIC LANGUAGE sql IMMUTABLE AS $$
  SELECT (cents::numeric / 100.0);
$$;

-- pct_change(old numeric, new numeric) -> numeric
-- Example: SELECT pct_change(100, 120); -- 0.20
CREATE OR REPLACE FUNCTION pct_change(old NUMERIC, new NUMERIC)
RETURNS NUMERIC LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE WHEN old = 0 THEN NULL ELSE (new - old) / old END;
$$;

-- label_percentile_rank(value numeric, arr numeric[], labels text[]) -> text
-- Returns a bucket label for a value relative to distribution arr.
-- labels length should match number of buckets; we split arr into equal-width quantiles.
-- Example:
--   SELECT label_percentile_rank(75, ARRAY[10,20,30,40,50,60,70,80,90], ARRAY['Low','Mid','High']);
--   -- 'High'
CREATE OR REPLACE FUNCTION label_percentile_rank(val NUMERIC, arr NUMERIC[], labels TEXT[])
RETURNS TEXT LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE n INT; q NUMERIC; i INT; p NUMERIC;
BEGIN
  IF arr IS NULL OR array_length(arr,1) IS NULL OR labels IS NULL THEN RETURN NULL; END IF;
  n := array_length(labels,1);
  IF n < 1 THEN RETURN NULL; END IF;
  -- Compute percentile of val among arr (inclusive rank / length)
  p := (SELECT (count(*) FILTER (WHERE x <= val))::numeric / NULLIF(count(*),0)
        FROM unnest(arr) x);
  IF p IS NULL THEN RETURN NULL; END IF;
  q := 1.0 / n;
  FOR i IN 1..n LOOP
    IF p <= i*q OR i = n THEN
      RETURN labels[i];
    END IF;
  END LOOP;
  RETURN labels[n];
END; $$;
