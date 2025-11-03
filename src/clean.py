import os
import re

DATA_RAW = "data/raw"
DATA_CLEAN = "data/cleaned"

def try_read(path):
    """To open the text file with fallback encodings."""

    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to decode {path} with apptoved encodings")

def extract_text(text: str, filename: str = "") -> str:
    """
    Generalized extraction across all Project Gutenberg regions for text between header and footer.
    """
    
    #explicit start and end markers (US style)
    start_pat = re.search(r"\*\*\*\s*START OF.*?\*\*\*", text, flags=re.IGNORECASE)
    end_pat   = re.search(r"\*\*\*\s*END OF.*?\*\*\*", text, flags=re.IGNORECASE)

    if start_pat and end_pat:
        return text[start_pat.end():end_pat.start()].strip()
    
    #if it doesnt work, try heuristics for AUS/CA
    start_idx = 0
    end_idx = len(text)

    #header
    header_match = re.search(r"(?im)^(?:Title:|CHAPTER\s+I\b|BOOK\s+ONE\b)", text)
    if header_match:
        start_idx = max(start_idx, header_match.start())

    #footer
    footer_match = re.search(
        r"(?im)(?:\*\*\*\s*END OF|THE END$|\[End of [^\]]+\]|Project Gutenberg(?: Australia| Canada))",
        text
    )
    if footer_match:
        end_idx = footer_match.start()

    body = text[start_idx:end_idx].strip()

    #safety check to prevent overtrimming
    if len(body) < 0.5 * len(text) * 0.05:  # <5% of original length
        print(f" {filename}: extraction too small ({len(body)} chars) — reverting to full text.")
        return text

    #common error license preamble for AU/CA
    body = re.sub(
        r"(?si)^\s*\*?\s*A\s+Project\s+Gutenberg\s+(?:of\s+Australia|Canada)\b.*?(?=(?:Title:|CHAPTER|BOOK\s+ONE))",
        "",
        body
    )
    return body


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_text(text: str, filename: str = "") -> str:
    original_len = len(text)
    text = extract_text(text, filename)
    #error handling, caused issues
    text = re.sub(r"End of (the )?Project Gutenberg.*", "", text, flags=re.IGNORECASE)
    text = normalize_whitespace(text)
    cleaned_len = len(text)
    reduction = 100 * (1 - cleaned_len / max(original_len, 1))
    print(f"   Original: {original_len:,} → Cleaned: {cleaned_len:,} ({reduction:.1f}% reduction)")
    return text

def clean_all_books():
    """
    Iterate through all raw directories, clean each file and save it to the clean directory.
    """

    if not os.path.exists(DATA_CLEAN):
        os.makedirs(DATA_CLEAN)

    for author in os.listdir(DATA_RAW):
        author_path = os.path.join(DATA_RAW, author)
        if not os.path.isdir(author_path):
            continue #skip the non directory files

        #create a matching folder in DATA_CLEAN
        cleaned_author_path = os.path.join(DATA_CLEAN, author)
        os.makedirs(cleaned_author_path, exist_ok=True)

        print(f"\n Cleaning author: {author}")
        for filename in os.listdir(author_path):
            if not filename.endswith(".txt"):
                continue

            raw_file = os.path.join(author_path, filename)
            cleaned_file = os.path.join(cleaned_author_path, filename.replace(".txt", "_clean.txt"))

            try:
                text, enc_used = try_read(raw_file)
                cleaned_text = clean_text(text, filename)

                with open(cleaned_file, "w", encoding="utf-8") as f:
                    f.write(cleaned_text)

                print(f"Cleaned: {filename} -> {cleaned_file}")

            except Exception as e:
                print(f"Error cleaning {filename}: {e}")

if __name__ == "__main__":
    clean_all_books()