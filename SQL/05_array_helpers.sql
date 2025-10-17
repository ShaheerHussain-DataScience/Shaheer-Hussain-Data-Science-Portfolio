
-- ============================================================================
-- ARRAY HELPERS
-- Intersections, differences, unique, compact NULLs.
-- ============================================================================
SET search_path = public;

-- array_unique(anyarray) -> anyarray
-- Example: SELECT array_unique(ARRAY[1,2,2,3,NULL,1]); -- {1,2,3,NULL}
CREATE OR REPLACE FUNCTION array_unique(anyarray)
RETURNS anyarray LANGUAGE sql IMMUTABLE AS $$
  SELECT ARRAY(SELECT DISTINCT x FROM unnest($1) AS x);
$$;

-- array_compact(anyarray) -> anyarray
-- Remove NULLs.
-- Example: SELECT array_compact(ARRAY[1,NULL,2,NULL,3]); -- {1,2,3}
CREATE OR REPLACE FUNCTION array_compact(anyarray)
RETURNS anyarray LANGUAGE sql IMMUTABLE AS $$
  SELECT ARRAY(SELECT x FROM unnest($1) x WHERE x IS NOT NULL);
$$;

-- array_intersect(anyarray, anyarray) -> anyarray
-- Example: SELECT array_intersect(ARRAY[1,2,3], ARRAY[2,3,4]); -- {2,3}
CREATE OR REPLACE FUNCTION array_intersect(a anyarray, b anyarray)
RETURNS anyarray LANGUAGE sql IMMUTABLE AS $$
  SELECT ARRAY(SELECT DISTINCT x FROM unnest(a) x INNER JOIN unnest(b) y ON x = y);
$$;

-- array_except(anyarray, anyarray) -> anyarray
-- Example: SELECT array_except(ARRAY[1,2,3], ARRAY[2]); -- {1,3}
CREATE OR REPLACE FUNCTION array_except(a anyarray, b anyarray)
RETURNS anyarray LANGUAGE sql IMMUTABLE AS $$
  SELECT ARRAY(SELECT x FROM unnest(a) x WHERE NOT x = ANY(b));
$$;
