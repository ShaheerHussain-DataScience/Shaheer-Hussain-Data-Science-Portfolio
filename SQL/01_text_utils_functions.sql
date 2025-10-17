
-- ============================================================================
-- TEXT UTILITIES (PostgreSQL)
-- Ready-to-use functions with simple signatures. Copy-paste and call directly.
-- Swap example literals/parameters in the examples to fit your use case.
-- ============================================================================
SET search_path = public;

-- normalize_text(text) -> text
-- Lowercase, trim, and collapse internal whitespace to single spaces.
-- Example:
--   SELECT normalize_text('  Alice   In   WondErland  ');
--   -- 'alice in wonderland'
CREATE OR REPLACE FUNCTION normalize_text(t TEXT)
RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
  SELECT regexp_replace(lower(btrim(t)), '\s+', ' ', 'g');
$$;

-- slugify(text) -> text
-- Create a URL-friendly slug from a free-form string.
-- Example:
--   SELECT slugify('Hello, World! PostgreSQL & You');
--   -- 'hello-world-postgresql-you'
CREATE OR REPLACE FUNCTION slugify(t TEXT)
RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
  SELECT regexp_replace(
           regexp_replace(normalize_text(t), '[^a-z0-9\s-]', '', 'g'),
           '\s+', '-', 'g'
         );
$$;

-- email_domain(text) -> text
-- Extract the domain portion of an email address. Returns NULL if invalid.
-- Example:
--   SELECT email_domain('alice@example.co.uk'); -- 'example.co.uk'
CREATE OR REPLACE FUNCTION email_domain(email TEXT)
RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE
           WHEN email ~ '^[^@]+@[^@]+\.[^@]+$' THEN split_part(email, '@', 2)
           ELSE NULL
         END;
$$;

-- extract_domain(text) -> text
-- Extract domain from a URL (basic heuristic). Returns NULL if no match.
-- Example:
--   SELECT extract_domain('https://sub.example.com/path?q=1'); -- 'sub.example.com'
CREATE OR REPLACE FUNCTION extract_domain(url TEXT)
RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
  SELECT NULLIF(regexp_replace(url, '^[a-z]+://([^/]+).*$','\1','i'), '');
$$;

-- left_pad(text, target_len, pad_char) -> text
-- Simple wrapper for LPAD but with safe handling of NULLs.
-- Example:
--   SELECT left_pad('42', 5, '0'); -- '00042'
CREATE OR REPLACE FUNCTION left_pad(val TEXT, target_len INT, pad_char TEXT DEFAULT '0')
RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE WHEN val IS NULL THEN NULL ELSE lpad(val, target_len, pad_char) END;
$$;
