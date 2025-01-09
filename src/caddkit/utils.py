from math import log10
from typing import Union


def ic50_to_pic50(ic50: Union[float, int], unit: str) -> float:
    """
    Converts IC50 value to pIC50 based on the provided unit.

    Parameters:
        ic50 (Union[float, int]): The IC50 value to be converted.
        unit (str): The unit of the IC50 value. Supported units are:
                    "nM" (nanomolar), "µM" (micromolar), "mM" (millimolar),
                    "M" (molar).

    Returns:
        float: The calculated pIC50 value.

    Raises:
        ValueError: If the IC50 value is non-positive or if the unit is
        invalid.
    """
    # Unit conversion factors to molar (M)
    unit_factors = {
        "nM": 1e-9,
        "µM": 1e-6,
        "mM": 1e-3,
        "M": 1
    }

    # Validate inputs
    if not isinstance(ic50, (float, int)) or ic50 <= 0:
        raise ValueError("IC50 value must be a positive number.")
    if unit not in unit_factors:
        raise ValueError(
            f"Invalid unit '{unit}'. Supported units are: "
            f"{', '.join(unit_factors.keys())}."
        )

    # Convert IC50 to molar concentration
    ic50_molar = ic50 * unit_factors[unit]

    # Calculate pIC50
    pic50 = -log10(ic50_molar)
    return pic50

