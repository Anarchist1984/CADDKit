import pandas as pd
from typing import Optional, Tuple
from caddkit.ml.ml_utils import split_data
from xgboost import XGBClassifier
import shap

class XGBoost:
    def __init__(self):
        pass

    @staticmethod
    def preprocess(data: pd.DataFrame, target_column: str, test_size: float = 0.2, random_state: Optional[int] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Preprocess the data by splitting it into training and testing sets.

        Args:
            data (pd.DataFrame): The input data.
            target_column (str): The name of the target column.
            test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
            random_state (Optional[int], optional): Controls the shuffling applied to the data before applying the split. Defaults to None.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: The training and testing data and target values.
        """
        try:
            X_train, X_test, y_train, y_test = split_data(data, target_column=target_column, test_size=test_size, random_state=random_state)
            return X_train, X_test, y_train, y_test
        except Exception as e:
            raise ValueError(f"Error in preprocessing data: {e}")

    @staticmethod
    def fit(X_train: pd.DataFrame, y_train: pd.Series, use_label_encoder: bool = False, eval_metric: str = "logloss", random_state: int = 42) -> XGBClassifier:
        """
        Fit the XGBoost model to the training data.

        Args:
            X_train (pd.DataFrame): The training data.
            y_train (pd.Series): The target values for the training data.
            use_label_encoder (bool, optional): Whether to use the label encoder. Defaults to False.
            eval_metric (str, optional): The evaluation metric. Defaults to "logloss".
            random_state (int, optional): The random state for reproducibility. Defaults to 42.

        Returns:
            XGBClassifier: The trained XGBoost model.
        """
        try:
            model = XGBClassifier(use_label_encoder=use_label_encoder, eval_metric=eval_metric, random_state=random_state)
            model.fit(X_train, y_train)
            return model
        except Exception as e:
            raise ValueError(f"Error in fitting model: {e}")

    @staticmethod
    def evaluate(model: XGBClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> float:
        """
        Evaluate the XGBoost model on the test data.

        Args:
            model (XGBClassifier): The trained XGBoost model.
            X_test (pd.DataFrame): The test data.
            y_test (pd.Series): The target values for the test data.

        Returns:
            float: The accuracy of the model on the test data.
        """
        try:
            model_accuracy = model.score(X_test, y_test)
            return model_accuracy
        except Exception as e:
            raise ValueError(f"Error in evaluating model: {e}")

def shap_analysis(model: XGBClassifier, X_test: pd.DataFrame):
    """
    Perform SHAP analysis on the XGBoost model.

    Args:
        model (XGBClassifier): The trained XGBoost model.
        X_test (pd.DataFrame): The test data.

    Returns:
        None: Displays the SHAP summary plot.
    """
    try:
        explainer_xg_morgan = shap.Explainer(model, X_test)
        shap_values_xg_morgan = explainer_xg_morgan(X_test)
        shap.summary_plot(shap_values_xg_morgan, X_test)
    except Exception as e:
        raise ValueError(f"Error in SHAP analysis: {e}")