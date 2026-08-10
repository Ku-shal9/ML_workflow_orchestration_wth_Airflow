import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def train_model(input_path, model_output_path):
    # Load cleaned dataset
    df = pd.read_csv(input_path)

    # Separate features and target
    X = df.drop("label", axis=1)
    y = df["label"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # Baseline Decision Tree
    dt_default = DecisionTreeClassifier(random_state=42)

    # Train model
    dt_default.fit(X_train, y_train)

    print("Decision Tree model trained successfully.")

    with open(model_output_path, "wb") as f:
        pickle.dump(dt_default, f)

    print(f"Model saved to {model_output_path}")

    return model_output_path
