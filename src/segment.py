import os
import re
import pandas as pd

DATA_CLEAN = "data/cleaned"
DATA_SEGMENTED = "data/segmented"
WORDS_PER_SEGMENT = 1500

def segment_text(text, words_per_segment=WORDS_PER_SEGMENT):
    """
    Split text into roughly equal segments of N words.
    """

    words = text.split()
    segments = []
    for i in range(0, len(words), words_per_segment):
        chunk = " ".join(words[i:i + words_per_segment])
        if len(chunk.split()) >= words_per_segment * 0.5: #drop small tails
            segments.append(chunk)
    return segments

def segment_all_books():
    if not os.path.exists(DATA_SEGMENTED):
        os.makedirs(DATA_SEGMENTED)

    rows = []
    for author in os.listdir(DATA_CLEAN):
        author_path = os.path.join(DATA_CLEAN, author)
        if not os.path.isdir(author_path):
            continue

        print(f"\nSegmenting author: {author}")
        out_author_path = os.path.join(DATA_SEGMENTED, author)
        os.makedirs(out_author_path, exist_ok=True)

        for filename in os.listdir(author_path):
            if not filename.endswith("_clean.txt"):
                continue

            filepath = os.path.join(author_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            title = re.sub(r"_clean\.txt$", "", filename).split("_", 1)
            segments = segment_text(text)

            print(f" - {filename}: {len(segments)} segments")

            for i, seg in enumerate(segments, start=1):
                seg_id = f"{os.path.splitext(filename)[0]}_seg{i:03d}"
                seg_file = os.path.join(out_author_path, f"{seg_id}.txt")

                with open(seg_file, "w", encoding="utf-8") as f:
                    f.write(seg)

                rows.append({
                    "author": author,
                    "title": title,
                    "segment_id": seg_id,
                    "text": seg,
                })

    df = pd.DataFrame(rows)
    csv_path = os.path.join(DATA_SEGMENTED, "modernist_corpus.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n Saved {len(df)} total segments to {csv_path}")

if __name__ == "__main__":
    segment_all_books()