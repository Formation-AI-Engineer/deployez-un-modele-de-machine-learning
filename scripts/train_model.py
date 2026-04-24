"""Train the CatBoost model and export it for the API.

Usage:
    python scripts/train_model.py

Produces: models/catboost_attrition.cbm
"""

import sys
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from catboost import CatBoostClassifier
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from app.preprocessing import encode_features, load_and_merge, prepare_features

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "catboost_attrition.cbm"


def main():
    print("Loading and merging datasets...")
    df = load_and_merge(
        sirh_path=str(DATA_DIR / "extrait_sirh.csv"),
        eval_path=str(DATA_DIR / "extrait_eval.csv"),
        sondage_path=str(DATA_DIR / "extrait_sondage.csv"),
    )
    print(f"  Merged dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    print("Preparing features...")
    X, y = prepare_features(df)

    print("Encoding features...")
    X = encode_features(X)
    print(f"  Feature matrix: {X.shape[0]} rows, {X.shape[1]} features")
    print(f"  Features: {list(X.columns)}")

    print("Splitting train/test (80/20, stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    print("Training CatBoost (baseline — defaults + auto_class_weights='Balanced')...")
    model = CatBoostClassifier(
        auto_class_weights="Balanced",
        random_seed=42,
        verbose=100,
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test).ravel().astype(int)
    y_proba = model.predict_proba(X_test)[:, 1]

    train_acc = model.score(X_train, y_train)
    test_acc = (y_pred == y_test.values).mean()
    pr_auc = average_precision_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

    print("\n=== Evaluation on held-out test set ===")
    print(f"  Train accuracy : {train_acc:.4f}")
    print(f"  Test accuracy  : {test_acc:.4f}")
    print(f"  PR AUC (Oui=1) : {pr_auc:.4f}")
    print("\nClassification report (0=Non, 1=Oui):")
    print(classification_report(y_test, y_pred, digits=3))
    print("Confusion matrix (rows=true, cols=pred; labels=[0=Non, 1=Oui]):")
    print(cm)

    # Save
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(str(MODEL_PATH))
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
