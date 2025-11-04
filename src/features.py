import os
import re
import numpy as np
import pandas as pd

from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize, pos_tag

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('average_perceptron_tagger')

DATA_SEGMENTED = "data/segmented"
INPUT_FILE = os.path.join(DATA_SEGMENTED, "corpus.csv")
OUTPUT_FILE = os.path.join(DATA_SEGMENTED, "corpus.csv")

STOPWORDS = set(stopwords.words('english'))

# feature groups

def lexical_features(text):
    tokens = [t.lower() for t in word_tokenize(text) if t.isalpha()]
    if not tokens:
        return {f"lex_{k}": 0 for k in ["word_len_avg", "ttr", "hapax_ratio", "stopword_ratio"]}
    
    lengths = [len(w) for w in tokens]
    word_len_avg = np.mean(lengths)
    ttr = len(set(tokens)) / len(tokens)
    hapax = sum(1 for w, c in Counter(tokens).items() if c == 1)
    hapax_ratio = hapax / len(tokens)
    stop_ratio = sum(1 for w in tokens if w in STOPWORDS) / len(tokens)

    return {
        "lex_word_len_avg": word_len_avg,
        "lex_ttr": ttr,
        "lex_hapax_ratio": hapax_ratio,
        "lex_stopword_ratio": stop_ratio, 
    }

def syntactic_features(text):
    sentences = sent_tokenize(text)
    sent_lens = [len(word_tokenize(s) for s in sentences if len(word_tokenize)) > 0]
    if not sent_lens:
        sent_lens = [0]

    punct_counts = Counter(re.findall(r"[;,:-\-\.!?", text))
    punct_total = sum(punct_counts.values())
    avg_sent_len = np.mean(sent_lens)
    sent_len_var = np.var(sent_lens)

    return {
        "syn_avg_sent_len": avg_sent_len,
        "syn_sent_len_var": sent_len_var,
        "syn_punct_per_1000": punct_total / (len(text.split()) / 1000 + 1e-6),
    }

def character_features(text):
    feats = {
        "char_semicolons": text.count(";"),
        "char_colons": text.count(":"),
        "char_emdashes": text.count("—") + text.count("--"),
        "char_ellipses": text.count("..."),
        "char_quotes": text.count('"') + text.count("'"),
        "char_exclaims": text.count("!"),
        "char_question": text.count("?")
    }

    total_chars = len(text)
    return {k: v / (total_chars / 1000 + 1e-6) for k, v in feats.items()}

def structural_features(text):
    paragraphs = [p for p in text.split("\n\n") if len(p.strip()) > 0]
    para_lens = [len(word_tokenize(p)) for p in paragraphs or [0]]
    avg_para_len = np.mean(para_lens)

    #dialogue ratio
    dialogues = re.findall(r"[\"“”'](.*?)[\"“”']", text)
    dialogue_tokens = sum(len(word_tokenize(d)) for d in dialogues)
    total_tokens = len(word_tokenize(text)) or 1
    dialogue_ratio = dialogue_tokens / total_tokens

    return {
        "str_avg_para_len": avg_para_len,
        "str_dialogue_ratio": dialogue_ratio,
    }


#pipeline time

def compute_features(df):
    records = []
    for i, row in df.iterrows():
        text = row["text"]

        f_lex = lexical_features(text)
        f_syn = syntactic_features(text)
        f_char = character_features(text)
        f_str = structural_features(text)

        feats = {**row.to_dict(), **f_lex, **f_syn, **f_char, **f_str}
        records.append(feats)

        if (i + 1) % 100 == 0:
            print(f"Processed {i+1}/{len(df)} segments")

    return pd.DataFrame(records)

def main():
    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} segments. Computing features...")

    features_df = compute_features(df)
    features_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved feature dataset to {OUTPUT_FILE}")
    print(f"Feature columns: {len(features_df.columns)}")

if __name__ == "__main__":
    main()