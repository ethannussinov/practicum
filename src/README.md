# clean.py

**Goal:** remove Gutenberg license headers/footers, normalize whitespace, and ensure UTF-8 consistency.

## key functions
- **`try_read(path)`** — opens each file using fallback encodings (`utf-8`, `latin-1`, `cp1252`).
- **`extract_text(text, filename)`** — detects `*** START OF ... ***` and `*** END OF ... ***` markers;  
  falls back to heuristic trimming for Australia/Canada editions.
- **`normalize_whitespace(text)`** — unifies newlines and spacing.
- **`clean_all_books()`** — iterates through `/data/raw`, cleans each file, and writes `/data/cleaned`.

## design choices
- Supports multiple regional Gutenberg formats.
- Includes safety checks: if extraction yields < 5 % of original length, the full text is preserved.
- Prints before/after character counts for transparency.
- Reductions of ~2–8 % indicate successful license removal without text loss.

## typical output ex
Cleaning author: Aldous Huxley
Original: 535,572 → Cleaned: 510,237 (4.7 % reduction)