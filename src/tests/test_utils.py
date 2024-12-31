import pytest
import math
import numpy as np
from molpharm.utils import convert_ic50_to_pic50

def test_valid_ic50():
    # Test with a valid IC50 value
    IC50_value = 1000  # IC50 in nM
    expected = 9 - math.log10(IC50_value)  # Expected pIC50 value
    result = convert_ic50_to_pic50(IC50_value)
    assert np.isclose(result, expected), f"Expected {expected}, but got {result}"

def test_zero_ic50():
    # Test with IC50 value equal to 0
    IC50_value = 0
    result = convert_ic50_to_pic50(IC50_value)
    assert np.isnan(result), f"Expected NaN, but got {result}"

def test_negative_ic50():
    # Test with a negative IC50 value
    IC50_value = -1000
    result = convert_ic50_to_pic50(IC50_value)
    assert np.isnan(result), f"Expected NaN, but got {result}"

def test_large_ic50():
    # Test with a very large IC50 value
    IC50_value = 1e6  # 1,000,000 nM
    expected = 9 - math.log10(IC50_value)
    result = convert_ic50_to_pic50(IC50_value)
    assert np.isclose(result, expected), f"Expected {expected}, but got {result}"

def test_invalid_ic50_type():
    # Test with an invalid type (string)
    IC50_value = "invalid"
    result = convert_ic50_to_pic50(IC50_value)
    assert np.isnan(result), f"Expected NaN, but got {result}"

def test_ic50_large_float():
    # Test with a very small IC50 value (close to 0)
    IC50_value = 1e-10
    expected = 9 - math.log10(IC50_value)
    result = convert_ic50_to_pic50(IC50_value)
    assert np.isclose(result, expected), f"Expected {expected}, but got {result}"

if __name__ == "__main__":
    pytest.main()