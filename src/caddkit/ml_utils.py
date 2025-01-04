from sklearn.model_selection import train_test_split
import pandas as pd

def split_data(df, target_column, test_size=0.2, random_state=None):
    """
    Splits a DataFrame into training and testing datasets, separating features (X) and target (y).

    Parameters:
        df (pd.DataFrame): The input DataFrame containing features and target.
        target_column (str): The name of the column to be used as the target variable (y).
        test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
        random_state (int, optional): Controls the shuffling applied to the data before the split. Defaults to None.

    Returns:
        tuple: Four DataFrames: X_train, X_test, y_train, y_test.

    Raises:
        ValueError: If the target column is not found in the DataFrame.
    """
    if target_column not in df.columns:
        raise ValueError(f"The target column '{target_column}' is not in the DataFrame.")
    
    print(f"Splitting data with test size {test_size}...")
    
    
    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Split into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"Data successfully split: {len(X_train)} train samples, {len(X_test)} test samples.")
    return X_train, X_test, y_train, y_test
