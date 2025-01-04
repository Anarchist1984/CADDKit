from lazypredict.Supervised import LazyRegressor
from lazypredict.Supervised import LazyClassifier
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class lazypredicthandler():
    def classifier_train(X_train, X_test, y_train, y_test):
        clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
        models,predictions = clf.fit(X_train, X_test, y_train, y_test)
        return models
    
    def regressor_train(X_train, X_test, y_train, y_test):
        reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
        models, predictions = reg.fit(X_train, X_test, y_train, y_test)
        return models
    

def visualize_lazy_performance(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    task: str = "regression",
    metric: str = "R-Squared",
    top_n: int = 10,
    palette: str = "viridis"
) -> Tuple[pd.DataFrame, None]:
    """
    Train models using LazyPredict and visualize top models' performance.

    Args:
        X_train (pd.DataFrame): Training feature data.
        X_test (pd.DataFrame): Testing feature data.
        y_train (pd.Series): Training target labels.
        y_test (pd.Series): Testing target labels.
        task (str): Type of task ("regression" or "classification"). Default is "regression".
        metric (str): Metric for model ranking (e.g., "R-Squared" for regression or "Accuracy" for classification).
        top_n (int): Number of top models to display. Default is 10.
        palette (str): Seaborn color palette for the graph. Default is "viridis".

    Returns:
        Tuple[pd.DataFrame, None]: DataFrame of model results and a displayed Seaborn bar plot.
    """
    if task not in ["regression", "classification"]:
        raise ValueError("Task must be either 'regression' or 'classification'.")

    # Train models using LazyPredict
    if task == "regression":
        reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
        models, _ = reg.fit(X_train, X_test, y_train, y_test)
    else:
        clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
        models, _ = clf.fit(X_train, X_test, y_train, y_test)

    # Sort models by the specified metric
    if metric not in models.columns:
        raise ValueError(f"Metric '{metric}' not found in model results.")
    top_models = models.sort_values(by=metric, ascending=False).head(top_n).reset_index()

    # Create the Seaborn bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_models, x=metric, y='Model', palette=palette)
    plt.title(f"Top {top_n} Models by {metric} ({task.capitalize()})")
    plt.xlabel(metric)
    plt.ylabel("Model")
    plt.tight_layout()
    plt.show()

    return models, None