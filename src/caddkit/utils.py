import math
import numpy as np

def convert_ic50_to_pic50(ic50_value):
    """
    Converts IC50 values to pIC50.
    
    Parameters:
    ----------
    ic50_value : float
        The IC50 value in nM.

    Returns:
    -------
    float
        The pIC50 value, or NaN if the IC50 value is invalid.
    """
    if not isinstance(ic50_value, (int, float)):
        raise TypeError(f"IC50 value must be a number, got {type(ic50_value).__name__}.")

    if ic50_value <= 0:
        raise ValueError(f"IC50 value must be positive, got {ic50_value}.")

    try:
        return 9 - math.log10(ic50_value)
    except (ValueError, OverflowError) as e:
        # Catch specific exceptions related to math operations
        print(f"Error converting IC50 {ic50_value}: {e}")
        return np.nan
