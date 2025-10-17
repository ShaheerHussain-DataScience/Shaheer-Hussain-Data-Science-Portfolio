
-- ============================================================================
-- JSONB HELPERS
-- Deep merge, safe getters, and set-by-path utilities.
-- ============================================================================
SET search_path = public;

-- jsonb_get_text(jsonb, key text) -> text
-- Safe one-level getter returning text (NULL if missing).
-- Example: SELECT jsonb_get_text('{"a":1,"b":"x"}'::jsonb,'b'); -- 'x'
CREATE OR REPLACE FUNCTION jsonb_get_text(doc JSONB, key TEXT)
RETURNS TEXT LANGUAGE sql IMMUTABLE AS $$
  SELECT doc ->> key;
$$;

-- jsonb_deep_merge(a jsonb, b jsonb) -> jsonb
-- Recursively merge b into a. Arrays from b replace arrays in a.
-- Example:
--   SELECT jsonb_deep_merge('{"a":{"x":1,"y":2}}','{"a":{"y":9,"z":3}}');
--   -- {"a":{"x":1,"y":9,"z":3}}
CREATE OR REPLACE FUNCTION jsonb_deep_merge(a JSONB, b JSONB)
RETURNS JSONB LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE k TEXT; v JSONB; result JSONB := a;
BEGIN
  IF a IS NULL THEN a := '{}'::jsonb; END IF;
  IF b IS NULL THEN RETURN a; END IF;
  IF jsonb_typeof(a) <> 'object' OR jsonb_typeof(b) <> 'object' THEN
    RETURN b;
  END IF;
  FOR k, v IN SELECT key, value FROM jsonb_each(b) LOOP
    IF result ? k AND jsonb_typeof(result->k) = 'object' AND jsonb_typeof(v) = 'object' THEN
      result := result || jsonb_build_object(k, jsonb_deep_merge(result->k, v));
    ELSE
      result := result || jsonb_build_object(k, v);
    END IF;
  END LOOP;
  RETURN result;
END; $$;

-- jsonb_set_deep(doc jsonb, path text[], value jsonb) -> jsonb
-- Set a nested path, creating objects as needed.
-- Example:
--   SELECT jsonb_set_deep('{}','{a,b,c}', '42'::jsonb);  -- {"a":{"b":{"c":42}}}
CREATE OR REPLACE FUNCTION jsonb_set_deep(doc JSONB, path TEXT[], value JSONB)
RETURNS JSONB LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE head TEXT; tail TEXT[];
BEGIN
  IF array_length(path,1) IS NULL THEN
    RETURN value;
  END IF;
  head := path[1];
  tail := path[2:array_length(path,1)];
  IF array_length(tail,1) IS NULL THEN
    RETURN (COALESCE(doc,'{}'::jsonb) || jsonb_build_object(head, value));
  ELSE
    RETURN (COALESCE(doc,'{}'::jsonb) ||
            jsonb_build_object(head, jsonb_set_deep(COALESCE(doc->head,'{}'::jsonb), tail, value)));
  END IF;
END; $$;
