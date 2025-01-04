import numpy as np
import math

def convert_ic50_to_pic50(IC50_value):
    """
    Converts IC50 values to pIC50.
    
    Parameters:
    ----------
    IC50_value : float
        The IC50 value in nM.

    Returns:
    -------
    float
        The pIC50 value, or NaN if the IC50 value is invalid.
    """
    try:
        if IC50_value > 0:  # Ensure IC50 is positive
            return 9 - math.log10(IC50_value)
        else:
            return np.nan  # Return NaN for invalid IC50 values
    except Exception as e:
        print(f"Error converting IC50 {IC50_value}: {e}")
        return np.nan  # Handle unexpected errors gracefully