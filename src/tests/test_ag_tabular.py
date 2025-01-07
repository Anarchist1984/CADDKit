import pytest
import pandas as pd
from autogluon.tabular import TabularPredictor
from tempfile import TemporaryDirectory
from caddkit.ml.automl.autogluontabular import AutoGluonTabular
import os

@pytest.fixture
def sample_data():
    """Provides a small dataset for testing."""
    data = {
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [5, 4, 3, 2, 1],
        "target": [0, 1, 0, 1, 0],
    }
    return pd.DataFrame(data)

def test_train(sample_data):
    """Tests the train method."""
    predictor = AutoGluonTabular.train(sample_data, target_column="target")
    assert isinstance(predictor, TabularPredictor)
    assert predictor.label == "target"

def test_train_invalid_target(sample_data):
    """Tests train method with an invalid target column."""
    with pytest.raises(ValueError, match="is not a column in train_data"):
        AutoGluonTabular.train(sample_data, target_column="invalid_column")

def test_train_invalid_data():
    """Tests train method with invalid data type."""
    with pytest.raises(TypeError, match="train_data must be a pandas DataFrame or TabularDataset"):
        AutoGluonTabular.train(["invalid_data"], target_column="target")

def test_test(sample_data):
    """Tests the test method."""
    predictor = AutoGluonTabular.train(sample_data, target_column="target")
    evaluation = AutoGluonTabular.test(predictor, sample_data)
    assert isinstance(evaluation, dict)  # Evaluate returns a dictionary

def test_test_invalid_data(sample_data):
    """Tests test method with invalid test data."""
    predictor = AutoGluonTabular.train(sample_data, target_column="target")
    with pytest.raises(TypeError, match="test_data must be a pandas DataFrame or TabularDataset"):
        AutoGluonTabular.test(predictor, "invalid_data")


def test_save_model(sample_data):
    """Tests the save_model method."""
    with TemporaryDirectory() as temp_dir:
        predictor = AutoGluonTabular.train(sample_data, target_column="target", path=temp_dir)
        AutoGluonTabular().save_model(predictor)
        assert len(os.listdir(temp_dir)) > 0

def test_save_invalid_model():
    """Tests save_model with an invalid model type."""
    with TemporaryDirectory() as temp_dir:
        with pytest.raises(TypeError, match="predictor must be an instance of TabularPredictor"):
            AutoGluonTabular().save_model("invalid_model")

def test_load_invalid_dir():
    """Tests load_model with an invalid directory."""
    with pytest.raises(TypeError, match="model_dir must be a string"):
        AutoGluonTabular().load_model(123)

def test_predict(sample_data):
    """Tests the predict method."""
    predictor = AutoGluonTabular.train(sample_data, target_column="target")
    predictions = AutoGluonTabular.predict(predictor, sample_data)
    assert isinstance(predictions, pd.Series)

def test_predict_invalid_data(sample_data):
    """Tests predict method with invalid data."""
    predictor = AutoGluonTabular.train(sample_data, target_column="target")
    with pytest.raises(TypeError, match="data must be a pandas DataFrame or TabularDataset"):
        AutoGluonTabular.predict(predictor, "invalid_data")
