import pytest
import pandas as pd
from caddkit.ml.ml_utils import split_data, combine_data

def test_split_data():
    # Create a sample DataFrame
    data = {
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [5, 4, 3, 2, 1],
        "target": [1, 0, 1, 0, 1],
    }
    df = pd.DataFrame(data)

    # Test valid split
    x_train, x_test, y_train, y_test = split_data(df, target_column="target", test_size=0.4, random_state=42)
    assert len(x_train) == 3
    assert len(x_test) == 2
    assert len(y_train) == 3
    assert len(y_test) == 2
    assert set(x_train.columns) == {"feature1", "feature2"}

    # Test invalid target column
    with pytest.raises(ValueError, match="The target column 'invalid_target' is not in the DataFrame."):
        split_data(df, target_column="invalid_target")

def test_combine_data():
    # Create sample data
    X = pd.DataFrame({"feature1": [1, 2], "feature2": [3, 4]})
    y = pd.Series([0, 1], name="target")

    # Test valid combine
    combined_df = combine_data(X, y)
    assert combined_df.shape == (2, 3)
    assert list(combined_df.columns) == ["feature1", "feature2", "target"]

    # Test type errors
    with pytest.raises(TypeError, match="X must be a pandas DataFrame."):
        combine_data([1, 2, 3], y)

    with pytest.raises(TypeError, match="y must be a pandas Series."):
        combine_data(X, [0, 1])

    # Test length mismatch
    y_invalid = pd.Series([0], name="target")
    with pytest.raises(ValueError, match="X and y must have the same number of rows."):
        combine_data(X, y_invalid)