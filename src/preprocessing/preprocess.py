import pandas as pd


def preprocess_data(input_path, output_path):
    # Load dataset
    df = pd.read_csv(input_path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Validate expected target column
    if "label" not in df.columns:
        raise ValueError("Expected target column 'label' not found")

    # Drop columns that do not provide useful information
    df = df.drop(columns=["ethnicity", "geographical_location"], errors="ignore")

    # Binary encoding
    binary_mappings = {
        "gender": {"Male": 1, "Female": 0},
        "dietary_habits": {"High_Salt": 1, "Low_Salt": 0},
        "endoscopic_images": {"Abnormal": 1, "Normal": 0},
        "biopsy_results": {"Positive": 1, "Negative": 0},
        "ct_scan": {"Positive": 1, "Negative": 0},
    }

    for col, mapping in binary_mappings.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    # Handle missing existing conditions
    if "existing_conditions" in df.columns:
        df["existing_conditions"] = df["existing_conditions"].fillna("Unknown")

        # One-hot encode existing conditions
        df = pd.get_dummies(df, columns=["existing_conditions"], drop_first=False)

    # Drop miRNA accession identifier
    df.drop(columns=["mature_mirna_acc"], inplace=True, errors="ignore")

    # One-hot encode categorical biological variables
    df = pd.get_dummies(
        df, columns=["mature_mirna_id", "target_symbol"], drop_first=False
    )

    # Drop gene identifier columns
    df.drop(columns=["target_entrez", "target_ensembl"], inplace=True, errors="ignore")

    # Save cleaned dataset
    df.to_csv(output_path, index=False)

    return output_path
