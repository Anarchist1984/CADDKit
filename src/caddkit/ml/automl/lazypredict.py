from typing import Tuple, Optional
import pandas as pd
from lazypredict.Supervised import LazyClassifier, LazyRegressor
from caddkit.ml.ml_utils import split_data

class LazyRegression:
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
    def fit(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series, verbose: int = 0, ignore_warnings: bool = True, custom_metric: Optional[callable] = None) -> LazyRegressor:
        """
        Fit the LazyRegressor model on the training data.

        Args:
            X_train (pd.DataFrame): The training data.
            X_test (pd.DataFrame): The testing data.
            y_train (pd.Series): The training target values.
            y_test (pd.Series): The testing target values.
            verbose (int, optional): Verbosity mode. Defaults to 0.
            ignore_warnings (bool, optional): Ignore warnings. Defaults to True.
            custom_metric (Optional[callable], optional): Custom metric function. Defaults to None.

        Returns:
            LazyRegressor: The fitted LazyRegressor model.
        """
        try:
            reg = LazyRegressor(verbose=verbose, ignore_warnings=ignore_warnings, custom_metric=custom_metric)
            reg.fit(X_train, X_test=X_test, y_train=y_train, y_test=y_test)
            return reg
        except Exception as e:
            raise ValueError(f"Error in fitting LazyRegressor: {e}")
        
    def run(self, data: pd.DataFrame, target_column: str, test_size: float = 0.2, random_state: Optional[int] = None, verbose: int = 0, ignore_warnings: bool = True, custom_metric: Optional[callable] = None) -> LazyRegressor:
        """
        Run the LazyRegressor model on the provided data.

        Args:
            data (pd.DataFrame): The input data.
            target_column (str): The name of the target column.
            test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
            random_state (Optional[int], optional): Controls the shuffling applied to the data before applying the split. Defaults to None.
            verbose (int, optional): Verbosity mode. Defaults to 0.
            ignore_warnings (bool, optional): Ignore warnings. Defaults to True.
            custom_metric (Optional[callable], optional): Custom metric function. Defaults to None.

        Returns:
            LazyRegressor: The fitted LazyRegressor model.
        """
        try:
            X_train, X_test, y_train, y_test = self.preprocess(data, target_column, test_size, random_state)
            reg = self.fit(X_train, X_test, y_train, y_test, verbose, ignore_warnings, custom_metric)
            return reg
        except Exception as e:
            raise ValueError(f"Error in running LazyRegressor: {e}")

class LazyClassification:
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
    def fit(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series, verbose: int = 0, ignore_warnings: bool = True, custom_metric: Optional[callable] = None) -> LazyClassifier:
        """
        Fit the LazyClassifier model on the training data.

        Args:
            X_train (pd.DataFrame): The training data.
            X_test (pd.DataFrame): The testing data.
            y_train (pd.Series): The training target values.
            y_test (pd.Series): The testing target values.
            verbose (int, optional): Verbosity mode. Defaults to 0.
            ignore_warnings (bool, optional): Ignore warnings. Defaults to True.
            custom_metric (Optional[callable], optional): Custom metric function. Defaults to None.

        Returns:
            LazyClassifier: The fitted LazyClassifier model.
        """
        try:
            clf = LazyClassifier(verbose=verbose, ignore_warnings=ignore_warnings, custom_metric=custom_metric)
            clf.fit(X_train, X_test=X_test, y_train=y_train, y_test=y_test)
            return clf
        except Exception as e:
            raise ValueError(f"Error in fitting LazyClassifier: {e}")
        

    def run(self, data: pd.DataFrame, target_column: str, test_size: float = 0.2, random_state: Optional[int] = None, verbose: int = 0, ignore_warnings: bool = True, custom_metric: Optional[callable] = None) -> LazyRegressor:
        """
        Run the LazyRegressor model on the provided data.

        Args:
            data (pd.DataFrame): The input data.
            target_column (str): The name of the target column.
            test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
            random_state (Optional[int], optional): Controls the shuffling applied to the data before applying the split. Defaults to None.
            verbose (int, optional): Verbosity mode. Defaults to 0.
            ignore_warnings (bool, optional): Ignore warnings. Defaults to True.
            custom_metric (Optional[callable], optional): Custom metric function. Defaults to None.

        Returns:
            LazyRegressor: The fitted LazyRegressor model.
        """
        try:
            X_train, X_test, y_train, y_test = self.preprocess(data, target_column, test_size, random_state)
            reg = self.fit(X_train, X_test, y_train, y_test, verbose, ignore_warnings, custom_metric)
            return reg
        except Exception as e:
            raise ValueError(f"Error in running LazyRegressor: {e}")