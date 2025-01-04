from autogluon.tabular import TabularDataset, TabularPredictor
import pandas as pd
from typing import Union

class AutoGluonTabularHandler:
    """
    A handler class to simplify the usage of AutoGluon TabularPredictor 
    for training, testing, and predicting with tabular data.
    """

    def __init__(self) -> None:
        """Initializes the AutoGluonTabularHandler class."""
        pass

    @staticmethod
    def combine_data(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """
        Combines feature data (X) and target data (y) into a single DataFrame.

        Args:
            X (pd.DataFrame): Feature data.
            y (pd.Series): Target labels.

        Returns:
            pd.DataFrame: Combined DataFrame with features and target labels.
        """
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame.")
        if not isinstance(y, pd.Series):
            raise TypeError("y must be a pandas Series.")
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of rows.")

        X.reset_index(drop=True, inplace=True)
        y.reset_index(drop=True, inplace=True)
        combined_df = pd.concat([X, y], axis=1)

        return combined_df

    @staticmethod
    def train(train_data: Union[pd.DataFrame, TabularDataset], target_column: str) -> TabularPredictor:
        """
        Trains an AutoGluon TabularPredictor on the provided training data.

        Args:
            train_data (pd.DataFrame or TabularDataset): Training data containing features and target.
            target_column (str): Name of the column to be predicted.

        Returns:
            TabularPredictor: A trained TabularPredictor object.
        """
        if not isinstance(train_data, (pd.DataFrame, TabularDataset)):
            raise TypeError("train_data must be a pandas DataFrame or TabularDataset.")
        if not isinstance(target_column, str):
            raise TypeError("target_column must be a string.")
        if target_column not in train_data.columns:
            raise ValueError(f"'{target_column}' is not a column in train_data.")

        try:
            predictor = TabularPredictor(label=target_column).fit(train_data)
            return predictor
        except Exception as e:
            raise RuntimeError(f"Error during training: {e}")

    @staticmethod
    def test(predictor: TabularPredictor, test_data: Union[pd.DataFrame, TabularDataset], silent: bool = True) -> None:
        """
        Evaluates a trained TabularPredictor on the test data.

        Args:
            predictor (TabularPredictor): Trained TabularPredictor object.
            test_data (pd.DataFrame or TabularDataset): Test data containing features and target.
            silent (bool): If True, suppresses additional output. Default is True.

        Returns:
            None
        """
        if not isinstance(predictor, TabularPredictor):
            raise TypeError("predictor must be an instance of TabularPredictor.")
        if not isinstance(test_data, (pd.DataFrame, TabularDataset)):
            raise TypeError("test_data must be a pandas DataFrame or TabularDataset.")

        try:
            evaluation = predictor.evaluate(test_data, silent=silent)
            print(evaluation)
            return evaluation
        except Exception as e:
            raise RuntimeError(f"Error during testing: {e}")
        
    def save_model(self, predictor: TabularPredictor, output_dir: str) -> None:
        """
        Saves a trained TabularPredictor to the specified directory.

        Args:
            predictor (TabularPredictor): Trained TabularPredictor object.
            output_dir (str): Directory to save the model to.

        Returns:
            None
        """
        if not isinstance(predictor, TabularPredictor):
            raise TypeError("predictor must be an instance of TabularPredictor.")
        if not isinstance(output_dir, str):
            raise TypeError("output_dir must be a string.")

        try:
            predictor.save(output_dir)
        except Exception as e:
            raise RuntimeError(f"Error saving model: {e}")
        
    def load_model(self, model_dir: str) -> TabularPredictor:
        """
        Loads a trained TabularPredictor from the specified directory.

        Args:
            model_dir (str): Directory containing the saved model.

        Returns:
            TabularPredictor: Loaded TabularPredictor object.
        """
        if not isinstance(model_dir, str):
            raise TypeError("model_dir must be a string.")

        try:
            predictor = TabularPredictor.load(model_dir)
            return predictor
        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")

    #Broken 
    def get_leaderboard(self, predictor: TabularPredictor) -> pd.DataFrame:
        """
        Retrieves the leaderboard of models from a trained TabularPredictor.

        Args:
            predictor (TabularPredictor): Trained TabularPredictor object.

        Returns:
            pd.DataFrame: Leaderboard of models with performance metrics.
        """
        if not isinstance(predictor, TabularPredictor):
            raise TypeError("predictor must be an instance of TabularPredictor.")

        try:
            leaderboard = predictor.leaderboard()
            return leaderboard
        except Exception as e:
            raise RuntimeError(f"Error getting leaderboard: {e}")

    @staticmethod
    def predict(predictor: TabularPredictor, data: Union[pd.DataFrame, TabularDataset]) -> pd.Series:
        """
        Makes predictions using a trained TabularPredictor.

        Args:
            predictor (TabularPredictor): Trained TabularPredictor object.
            data (pd.DataFrame or TabularDataset): Data to make predictions on.

        Returns:
            pd.Series: Predicted values.
        """
        if not isinstance(predictor, TabularPredictor):
            raise TypeError("predictor must be an instance of TabularPredictor.")
        if not isinstance(data, (pd.DataFrame, TabularDataset)):
            raise TypeError("data must be a pandas DataFrame or TabularDataset.")

        try:
            predictions = predictor.predict(data)
            return predictions
        except Exception as e:
            raise RuntimeError(f"Error during prediction: {e}")
