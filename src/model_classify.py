import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

DATA_SEGMENTED = "data/segmented"
INPUT_FILE = os.path.join(DATA_SEGMENTED, "corpus.csv")

def load_data():
    df = pd.read_csv(INPUT_FILE)
    meta_cols = ["author", "title", "segment_id", "text"]
    feature_cols = [c for c in df.columns if c not in meta_cols]
    X = df[feature_cols].fillna(0)
    y = df["author"]
    return df, X, y, feature_cols

def evaluate_model(model, X_train, X_test, y_train, y_test, le, model_name):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"\n=== {model_name} Classification Report ===")
    print(classification_report(y_test, preds, target_names=le.classes_))
    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(7,6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=le.classes_, yticklabels=le.classes_)
    plt.title(f"{model_name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    out_path = os.path.join(DATA_SEGMENTED, f"{model_name.lower()}_confusion.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved confusion matrix to {out_path}")

def run_classification():
    df, X, y, feature_cols = load_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, stratify=y_encoded, random_state=13
    )

    #logistic regression
    logreg = LogisticRegression(max_iter=1000, multi_class="multinomial")
    evaluate_model(logreg, X_train, X_test, y_train, y_test, le, "LogisticRegression")

    #feature importance (avg abs coefficietns)
    importance = pd.Series(np.mean(np.abs(logreg.coef_), axis=0), index=feature_cols)
    top_feats = importance.sort_values(ascending=False).head(15)
    print("\nTop Features (LogReg):")
    print(top_feats)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_feats.values, y=top_feats.index)
    plt.title("Top Stylometric Features (LogReg)")
    plt.tight_layout()
    plt.savefig(os.path.join(DATA_SEGMENTED, "top_features_logreg.png"))
    plt.close()

    #random forest
    rf = RandomForestClassifier(n_estimators=200, random_state=13)
    evaluate_model(rf, X_train, X_test, y_train, y_test, le, "RandomForest")

    #cross validation baseline
    scores = cross_val_score(logreg, X_scaled, y_encoded, cv=5)
    print(f"\nCross-val mean accuracy (LogReg): {scores.mean():.3f} ± {scores.std():.3f}")

def main():
    run_classification()

if __name__ == "__main__":
    main()