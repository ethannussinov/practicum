import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

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

def visualize_pca_3d(df, feature_cols, output_dir="data/segmented"):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])

    pca = PCA(n_components=3)
    comps = pca.fit_transform(X_scaled)
    explained = pca.explained_variance_ratio_ * 100

    pca_df = pd.DataFrame({
        "PC1": comps[:, 0],
        "PC2": comps[:, 1],
        "PC3": comps[:, 2],
        "author": df["author"]
    })

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')
    palette = sns.color_palette("Set2", n_colors=len(pca_df["author"].unique()))

    for i, author in enumerate(pca_df["author"].unique()):
        points = pca_df[pca_df["author"] == author]
        ax.scatter(
            points["PC1"], points["PC2"], points["PC3"],
            label=author, s=40, alpha=0.6, color=palette[i]
        )

    ax.set_xlabel(f"PC1 ({explained[0]:.1f}%)")
    ax.set_ylabel(f"PC2 ({explained[1]:.1f}%)")
    ax.set_zlabel(f"PC3 ({explained[2]:.1f}%)")
    ax.set_title("3D PCA of Stylometric Features")
    ax.legend(loc="upper left")
    plt.tight_layout()

    out_path = os.path.join(output_dir, "pca_authors_3d.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved 3D PCA visualization to {out_path}")

def compute_pca_loadings(df, feature_cols, n_components=3, output_dir="data/segmented"):
    """
    Computes and saves PCA loadings (feature contributions) for interpretation.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    pca = PCA(n_components=n_components)
    pca.fit(X_scaled)

    loadings = pd.DataFrame(
        pca.components_.T,
        index=feature_cols,
        columns=[f"PC{i+1}" for i in range(n_components)]
    )

    explained = pca.explained_variance_ratio_ * 100
    print("\n=== PCA Explained Variance ===")
    for i, var in enumerate(explained, 1):
        print(f"PC{i}: {var:.2f}%")

    print("\n=== Top Contributing Features ===")
    for i in range(n_components):
        top_features = loadings.iloc[:, i].abs().sort_values(ascending=False).head(5)
        print(f"PC{i+1}: {', '.join(top_features.index)}")

    out_path = os.path.join(output_dir, "pca_loadings.csv")
    loadings.to_csv(out_path)
    print(f"\nSaved PCA loadings to {out_path}")
    return loadings, explained

def visualize_pca_biplot(df, feature_cols, output_dir="data/segmented"):
    """
    2D PCA biplot showing author clusters + top feature vectors.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    pca = PCA(n_components=2)
    comps = pca.fit_transform(X_scaled)
    explained = pca.explained_variance_ratio_ * 100

    pca_df = pd.DataFrame({
        "PC1": comps[:, 0],
        "PC2": comps[:, 1],
        "author": df["author"]
    })

    #create scatter plot
    plt.figure(figsize=(9, 7))
    sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="author", palette="Set2", s=60, alpha=0.7)

    #overlay feature loadings
    loadings = pca.components_.T
    feature_vectors = 4 * loadings  #scale arrows for visibility
    for i, f in enumerate(feature_cols):
        plt.arrow(0, 0, feature_vectors[i, 0], feature_vectors[i, 1],
                  color='gray', alpha=0.5, head_width=0.05)
        plt.text(feature_vectors[i, 0]*1.15, feature_vectors[i, 1]*1.15,
                 f, fontsize=8, ha='center', va='center', color='black', alpha=0.7)

    plt.xlabel(f"PC1 ({explained[0]:.1f}% variance)")
    plt.ylabel(f"PC2 ({explained[1]:.1f}% variance)")
    plt.title("PCA Biplot: Stylometric Feature Directions")
    plt.tight_layout()

    out_path = os.path.join(output_dir, "pca_biplot.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved PCA biplot to {out_path}")


def visualize_correlation(df, feature_cols):
    corr = df[feature_cols].corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
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
    visualize_pca_3d(df, feature_cols)
    visualize_correlation(df, feature_cols)
    visualize_feature_distributions(df, feature_cols)


    loadings, explained = compute_pca_loadings(df, feature_cols)
    visualize_pca_biplot(df, feature_cols)

if __name__ == "__main__":
    main()