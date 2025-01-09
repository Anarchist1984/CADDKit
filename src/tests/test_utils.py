import math
import numpy as np
import pytest
from caddkit.utils import ic50_to_pic50

def test_valid_ic50():
    # Test with a valid IC50 value in nM
    IC50_value = 1000  # IC50 in nM
    unit = "nM"
    expected = 9 - math.log10(IC50_value)  # Expected pIC50 value
    result = ic50_to_pic50(IC50_value, unit)
    assert np.isclose(result, expected), f"Expected {expected}, but got {result}"

def test_zero_ic50():
    # Test with IC50 value equal to 0
    IC50_value = 0
    unit = "nM"
    with pytest.raises(ValueError, match="IC50 value must be a positive number."):
        ic50_to_pic50(IC50_value, unit)

def test_negative_ic50():
    # Test with a negative IC50 value
    IC50_value = -1000
    unit = "nM"
    with pytest.raises(ValueError, match="IC50 value must be a positive number."):
        ic50_to_pic50(IC50_value, unit)

def test_large_ic50():
    # Test with a very large IC50 value in nM
    IC50_value = 1e6  # 1,000,000 nM
    unit = "nM"
    expected = 9 - math.log10(IC50_value)
    result = ic50_to_pic50(IC50_value, unit)
    assert np.isclose(result, expected), f"Expected {expected}, but got {result}"

def test_invalid_ic50_type():
    # Test with an invalid type (string)
    IC50_value = "invalid"
    unit = "nM"
    with pytest.raises(ValueError, match="IC50 value must be a positive number."):
        ic50_to_pic50(IC50_value, unit)

def test_invalid_unit():
    # Test with an invalid unit
    IC50_value = 1000
    unit = "ppm"  # Unsupported unit
    with pytest.raises(ValueError, match="Invalid unit 'ppm'. Supported units are: nM, µM, mM, M."):
        ic50_to_pic50(IC50_value, unit)

def test_very_small_ic50():
    # Test with a very small IC50 value in nM (close to 0, but positive)
    IC50_value = 1e-10
    unit = "M"  # Molar
    expected = -math.log10(IC50_value)
    result = ic50_to_pic50(IC50_value, unit)
    assert np.isclose(result, expected), f"Expected {expected}, but got {result}"