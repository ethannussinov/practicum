import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

DATA_SEGMENTED = "data/segmented"
INPUT_FILE = os.path.join(DATA_SEGMENTED, "corpus.csv")

def load_data():
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} segments from {INPUT_FILE}")
    meta_cols = ["author", "title", "segment_id", "text"]
    feature_cols = [c for c in df.columns if c not in meta_cols]
    return df, feature_cols

def feature_summary(df, feature_cols):
    print("\n=== Feature Summary (means by author) ===")
    summary = df.groupby("author")[feature_cols].mean().round(3)
    print(summary.head())
    out_path = os.path.join(DATA_SEGMENTED, "feature_summary.csv")
    summary.to_csv(out_path)
    print(f"Saved feature summary to {out_path}")

def visualize_pca(df, feature_cols):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    pca = PCA(n_components=2)
    comps = pca.fit_transform(X_scaled)
    pca_df = pd.DataFrame({"PC1": comps[:, 0], "PC2": comps[:, 1], "author": df["author"]})
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="author", palette="Set2", s=60, alpha=0.8)
    plt.title("PCA of Stylometric Features by Author")
    plt.tight_layout()
    out_path = os.path.join(DATA_SEGMENTED, "pca_authors.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved PCA visualization to {out_path}")

def visualize_correlation(df, feature_cols):
    corr = df[feature_cols].corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Feature Correlation Heatmap")
    plt.title_layout()
    out_path = os.path.join(DATA_SEGMENTED, "feature_correlation.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved feature correlation heatmap to {out_path}")

def visualize_feature_distributions(df, feature_cols):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="author", y="lex_ttr")
    plt.xticks(rotation=45)
    plt.title("Lexical Diversity (TTR) by Author")
    plt.tight_layout()
    out_path = os.path.join(DATA_SEGMENTED, "ttr_by_author.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved feature distribution plot to {out_path}")

def main():
    df, feature_cols = load_data()
    feature_summary(df, feature_cols)
    visualize_pca(df, feature_cols)
    visualize_correlation(df, feature_cols)
    visualize_feature_distributions(df, feature_cols)

if __name__ == "__main__":
    main()