#!/usr/bin/env python3
"""
Predictive analytics on scikit-learn's Breast Cancer dataset with 5 visuals.

- Trains Logistic Regression and Random Forest
- Prints metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
- Selects best model by ROC-AUC on test set
- Saves charts locally to ./downloads/
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    roc_curve, confusion_matrix
)


# -------------------------
# Helpers
# -------------------------
def ensure_dir(path="downloads"):
    os.makedirs(path, exist_ok=True)
    return path


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    data = load_breast_cancer(as_frame=True)
    X = data.data.copy()
    y = pd.Series(data.target, name="target")
    # Map targets for clarity (0=malignant, 1=benign)
    target_names = {i: name for i, name in enumerate(data.target_names)}
    y_named = y.map(target_names)
    return X, y, y_named


def train_models(X: pd.DataFrame, y: pd.Series, random_state: int = 42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=random_state
    )

    logreg = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=500, random_state=random_state))
        ]
    )

    rf = RandomForestClassifier(
        n_estimators=400,
        max_depth=None,
        n_jobs=-1,
        random_state=random_state
    )

    logreg.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    preds = {}
    for name, model in [("LogisticRegression", logreg), ("RandomForest", rf)]:
        y_prob = model.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_prob),
            "y_pred": y_pred,
            "y_prob": y_prob
        }
        preds[name] = metrics

    # Pick best by ROC-AUC
    best_name = max(preds.keys(), key=lambda n: preds[n]["roc_auc"])
    best_model = logreg if best_name == "LogisticRegression" else rf

    return (X_train, X_test, y_train, y_test), {"LogisticRegression": logreg, "RandomForest": rf}, preds, best_name, best_model


# -------------------------
# Visuals
# -------------------------
def fig1_class_balance(y_named: pd.Series, outdir: str):
    counts = y_named.value_counts().sort_index()
    plt.figure(figsize=(7, 5))
    plt.bar(counts.index, counts.values)
    plt.title("Class Balance")
    plt.xlabel("Class")
    plt.ylabel("Count")
    for i, v in enumerate(counts.values):
        plt.text(i, v, str(v), ha="center", va="bottom")
    plt.tight_layout()
    path = os.path.join(outdir, "01_class_balance.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig2_correlation_heatmap(X: pd.DataFrame, outdir: str, top_n: int = 20):
    """
    Correlation heatmap of the top_n features by overall absolute correlation sum
    (keeps heatmap readable vs 30x30).
    """
    corr = X.corr(numeric_only=True)
    abs_strength = corr.abs().sum().sort_values(ascending=False)
    keep = abs_strength.index[:top_n]
    corr_small = corr.loc[keep, keep].values

    plt.figure(figsize=(8, 7))
    im = plt.imshow(corr_small, aspect="auto")
    plt.title(f"Feature Correlation (Top {top_n})")
    plt.xticks(ticks=np.arange(len(keep)), labels=keep, rotation=90)
    plt.yticks(ticks=np.arange(len(keep)), labels=keep)
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Correlation")
    plt.tight_layout()
    path = os.path.join(outdir, "02_correlation_heatmap.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig3_roc_curves(models: dict, preds: dict, y_test: pd.Series, outdir: str):
    plt.figure(figsize=(7, 5))
    for name in ["LogisticRegression", "RandomForest"]:
        y_prob = preds[name]["y_prob"]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc = preds[name]["roc_auc"]
        plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title("ROC Curves (Test Set)")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.tight_layout()
    path = os.path.join(outdir, "03_roc_curves.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig4_confusion_matrix(best_name: str, preds: dict, y_test: pd.Series, outdir: str):
    cm = confusion_matrix(y_test, preds[best_name]["y_pred"])
    plt.figure(figsize=(6, 5))
    im = plt.imshow(cm, interpolation="nearest", aspect="auto")
    plt.title(f"Confusion Matrix ({best_name})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks([0, 1], ["Malignant(0)", "Benign(1)"])
    plt.yticks([0, 1], ["Malignant(0)", "Benign(1)"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j], ha="center", va="center")
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    path = os.path.join(outdir, "04_confusion_matrix.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig5_feature_importance(best_name: str, best_model, X: pd.DataFrame, outdir: str, top_k: int = 10):
    # Extract feature importances or coefficients
    if best_name == "RandomForest":
        importances = best_model.feature_importances_
        names = np.array(X.columns)
        values = importances
        title = "Feature Importance (Random Forest)"
    else:
        # Logistic Regression coefficients (absolute value for magnitude)
        # Model is a Pipeline(scaler, clf); get coef_ from final step
        clf = best_model.named_steps["clf"]
        coefs = np.abs(clf.coef_).ravel()
        names = np.array(X.columns)
        values = coefs
        title = "Coefficient Magnitudes (Logistic Regression)"

    idx = np.argsort(values)[::-1][:top_k]
    top_names = names[idx]
    top_vals = values[idx]

    plt.figure(figsize=(8, 5))
    plt.barh(range(len(top_vals)), top_vals[::-1])
    plt.yticks(range(len(top_names)), top_names[::-1])
    plt.title(f"{title} — Top {top_k}")
    plt.xlabel("Importance" if best_name == "RandomForest" else "Abs(Coefficient)")
    plt.tight_layout()
    path = os.path.join(outdir, "05_top_features.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


# -------------------------
# Main
# -------------------------
def main():
    outdir = ensure_dir("downloads")
    X, y, y_named = load_data()
    (X_train, X_test, y_train, y_test), models, preds, best_name, best_model = train_models(X, y)

    # Print metrics
    print("\n=== Test Metrics ===")
    for name in preds:
        m = preds[name]
        print(f"\n{name}")
        print(f"  Accuracy : {m['accuracy']:.3f}")
        print(f"  Precision: {m['precision']:.3f}")
        print(f"  Recall   : {m['recall']:.3f}")
        print(f"  F1-Score : {m['f1']:.3f}")
        print(f"  ROC-AUC  : {m['roc_auc']:.3f}")

    print(f"\nBest model by ROC-AUC: {best_name}")

    # Visuals
    print("\nSaving visuals locally to:", os.path.abspath(outdir), "\n")
    saved = []
    saved.append(fig1_class_balance(y_named, outdir))
    saved.append(fig2_correlation_heatmap(X, outdir, top_n=20))
    saved.append(fig3_roc_curves(models, preds, y_test, outdir))
    saved.append(fig4_confusion_matrix(best_name, preds, y_test, outdir))
    saved.append(fig5_feature_importance(best_name, best_model, X, outdir, top_k=10))

    print("✅ Visuals saved:")
    for p in saved:
        print(" -", os.path.abspath(p))


if __name__ == "__main__":
    main()
