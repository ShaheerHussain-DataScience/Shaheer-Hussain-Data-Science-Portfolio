
-- ============================================================================
-- DATE/TIME UTILITIES
-- Business-day math, month boundaries, bucketing helpers.
-- ============================================================================
SET search_path = public;

-- month_start(date) -> date
-- Example: SELECT month_start(date '2025-10-17'); -- '2025-10-01'
CREATE OR REPLACE FUNCTION month_start(d DATE)
RETURNS DATE LANGUAGE sql IMMUTABLE AS $$
  SELECT date_trunc('month', d)::date;
$$;

-- month_end(date) -> date
-- Example: SELECT month_end(date '2025-10-17'); -- '2025-10-31'
CREATE OR REPLACE FUNCTION month_end(d DATE)
RETURNS DATE LANGUAGE sql IMMUTABLE AS $$
  SELECT (date_trunc('month', d) + INTERVAL '1 month - 1 day')::date;
$$;

-- time_bucket_min(timestamptz, bucket_minutes int) -> timestamptz
-- Floor a timestamp to the start of the N-minute bucket.
-- Example: SELECT time_bucket_min('2025-10-17 12:07+00', 15); -- '2025-10-17 12:00+00'
CREATE OR REPLACE FUNCTION time_bucket_min(ts TIMESTAMPTZ, bucket_minutes INT)
RETURNS TIMESTAMPTZ LANGUAGE sql IMMUTABLE AS $$
  SELECT date_trunc('minute', ts)
         - make_interval(mins => (extract(minute FROM ts)::int % GREATEST(bucket_minutes,1)));
$$;

-- business_days_diff(start_date, end_date, holidays date[]) -> int
-- Count business days between dates (inclusive), ignoring weekends and supplied holidays.
-- Example:
--   SELECT business_days_diff('2025-10-01','2025-10-07', ARRAY['2025-10-03'::date]);
--   -- returns 4 (Oct 1,2,6,7) if Oct 3 is a holiday
CREATE OR REPLACE FUNCTION business_days_diff(start_date DATE, end_date DATE, holidays DATE[] DEFAULT ARRAY[]::DATE[])
RETURNS INT
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE d DATE; cnt INT := 0;
BEGIN
  IF start_date IS NULL OR end_date IS NULL THEN RETURN NULL; END IF;
  IF end_date < start_date THEN
    RETURN -business_days_diff(end_date, start_date, holidays);
  END IF;
  d := start_date;
  WHILE d <= end_date LOOP
    IF extract(isodow FROM d) < 6 AND NOT d = ANY(holidays) THEN
      cnt := cnt + 1;
    END IF;
    d := d + INTERVAL '1 day';
  END LOOP;
  RETURN cnt;
END;
$$;

-- working_minutes_between(timestamptz, timestamptz, start_hour int, end_hour int, holidays date[]) -> int
-- Count minutes between two timestamps that fall inside business hours on business days.
-- Hours are in 0-23 (local time of the timestamptz). Weekends & holidays excluded.
-- Example:
--   SELECT working_minutes_between('2025-10-01 08:15+00','2025-10-02 11:45+00',9,17,ARRAY[]::date[]);
--   -- counts minutes within 09:00–17:00 on Wed and Thu
CREATE OR REPLACE FUNCTION working_minutes_between(ts_start TIMESTAMPTZ,
                                                   ts_end   TIMESTAMPTZ,
                                                   start_hour INT DEFAULT 9,
                                                   end_hour   INT DEFAULT 17,
                                                   holidays DATE[] DEFAULT ARRAY[]::DATE[])
RETURNS INT
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE cur DATE; total INT := 0;
        day_start TIMESTAMPTZ; day_end TIMESTAMPTZ;
        win_start TIMESTAMPTZ; win_end TIMESTAMPTZ;
BEGIN
  IF ts_start IS NULL OR ts_end IS NULL THEN RETURN NULL; END IF;
  IF ts_end < ts_start THEN
    RETURN -working_minutes_between(ts_end, ts_start, start_hour, end_hour, holidays);
  END IF;

  cur := ts_start::date;
  WHILE cur <= ts_end::date LOOP
    IF extract(isodow FROM cur) < 6 AND NOT cur = ANY(holidays) THEN
      day_start := make_timestamptz(extract(year from cur)::int, extract(month from cur)::int, extract(day from cur)::int, start_hour, 0, 0);
      day_end   := make_timestamptz(extract(year from cur)::int, extract(month from cur)::int, extract(day from cur)::int, end_hour,   0, 0);

      win_start := GREATEST(day_start, date_trunc('day', ts_start) = cur::timestamp ? ts_start : day_start);
      win_end   := LEAST(day_end, date_trunc('day', ts_end) = cur::timestamp ? ts_end : day_end);

      -- GREATEST/LEAST above may not compile with ternary; rewrite safely:
    END IF;
    cur := cur + INTERVAL '1 day';
  END LOOP;
  -- Because PL/pgSQL doesn't support ternary directly, re-implement the window per day:
  total := 0;
  cur := ts_start::date;
  WHILE cur <= ts_end::date LOOP
    IF extract(isodow FROM cur) < 6 AND NOT cur = ANY(holidays) THEN
      day_start := make_timestamptz(extract(year from cur)::int, extract(month from cur)::int, extract(day from cur)::int, start_hour, 0, 0);
      day_end   := make_timestamptz(extract(year from cur)::int, extract(month from cur)::int, extract(day from cur)::int, end_hour,   0, 0);

      IF cur = ts_start::date THEN
        win_start := GREATEST(day_start, ts_start);
      ELSE
        win_start := day_start;
      END IF;

      IF cur = ts_end::date THEN
        win_end := LEAST(day_end, ts_end);
      ELSE
        win_end := day_end;
      END IF;

      IF win_end > win_start THEN
        total := total + EXTRACT(EPOCH FROM (win_end - win_start))::int / 60;
      END IF;
    END IF;
    cur := cur + INTERVAL '1 day';
  END LOOP;
  RETURN total;
END;
$$;
