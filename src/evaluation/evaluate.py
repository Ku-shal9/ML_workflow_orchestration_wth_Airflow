import pickle
import json

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


def evaluate_model(
    dataset_path,
    model_path,
    metrics_output_path,
):
    # Load cleaned dataset
    df = pd.read_csv(dataset_path)

    # Separate features and target
    X = df.drop("label", axis=1)
    y = df["label"]

    # Recreate the same train-test split used during training
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # Load trained model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    report = classification_report(
        y_test,
        y_pred,
        output_dict=True,
    )

    cm = confusion_matrix(y_test, y_pred)

    # ROC-AUC requires probability predictions
    y_proba = model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_proba)

    metrics = {
        "accuracy": report["accuracy"],
        "precision": report["weighted avg"]["precision"],
        "recall": report["weighted avg"]["recall"],
        "f1_score": report["weighted avg"]["f1-score"],
        "roc_auc": roc_auc,
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }

    # Save metrics
    with open(metrics_output_path, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Model evaluation completed.")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"Metrics saved to: {metrics_output_path}")

    return metrics_output_path
