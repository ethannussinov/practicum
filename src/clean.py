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

    start_patterns = [
        r"\*\*\*\s*START OF[^\n]*\n",
        r"PROJECT GUTENBERG(?:\s+OF)?\s+[A-Z][^\n]*EBOOK",
        r"Project Gutenberg Australia",
        r"Project Gutenberg Canada",
    ]
    end_patterns = [
        r"\*\*\*\s*END OF[^\n]*",
        r"\[End of [^\]]+\]",
        r"THE END\s*$",
        r"End of (the )?Project Gutenberg[^\n]*",
        r"Project Gutenberg Australia",
        r"Project Gutenberg Canada",
    ]

    start_idx, end_idx = 0, len(text)

    for sp in start_patterns:
        m = re.search(sp, text, flags=re.IGNORECASE)
        if m: 
            start_idx = max(start_idx, m.end())
    
    for ep in end_patterns:
        m = re.search(ep, text[start_idx], flags = re.IGNORECASE)
        if m:
            end_idx = start_idx + m.start()
            break

    body = text[start_idx:end_idx].strip()
    if start_idx == 0 and end_idx == len(text):
        print(f"No recognizable markers in {filename} - text kept the same.")
        return text
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
                with open(raw_file, "r", encoding="utf-8") as f:
                    text = f.read()

                cleaned_text = clean_text(text)

                with open(cleaned_file, "w", encoding="utf-8") as f:
                    f.write(cleaned_text)

                print(f"Cleaned: {filename} -> {cleaned_file}")

            except Exception as e:
                print(f"Error cleaning {filename}: {e}")

if __name__ == "__main__":
    clean_all_books()