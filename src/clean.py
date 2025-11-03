import os
import re

DATA_RAW = "data/raw"
DATA_CLEAN = "data/cleaned"

def clean_text(text: str) -> str:
    """
    Clean the downloaded Project Gutenberg text by removing headers, footers, license text, and normalizing whitespace
    """

    #remove Gutenberg header and footer
    text = re.sub(r"\*\*\* START OF.*?\*\*\*", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\*\*\* END OF.?\*\*\*", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"End of the Project Gutenberg.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Project Gutenberg.*", "", text, flags=re.IGNORECASE)

    #remove non alphabetic characters that slipped through
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,", "\n", text)
    text = re.sub(r"\s+", " ", text).strip()

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

        #create a mtching folder in DATA_CLEAN
        cleaned_author_path = os.path.join(DATA_CLEAN, author)
        os.makedirs(cleaned_author_path, exist_ok=True)

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