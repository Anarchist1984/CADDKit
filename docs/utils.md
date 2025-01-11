```python
from caddkit import utils
```

## Function: `ic50_to_pic50`

```python
ic50_to_pic50(ic50: Union[float, int], unit: str) -> float
```

### Description
Converts an IC50 value to a pIC50 value using the specified unit of measurement. The pIC50 value is a logarithmic measure indicating the potency of a compound in pharmacology.

### Notes
- IC50 values should be provided in one of the supported units for accurate conversion.
- Base-10 logarithms are used for the calculation.

### Supported Units
| Unit   | Conversion Factor to Molar (M) |
|--------|---------------------------------|
| `nM`   | `1e-9`                         |
| `µM`   | `1e-6`                         |
| `mM`   | `1e-3`                         |
| `M`    | `1`                            |

### Arguments
- **`ic50`** (`Union[float, int]`):  
    The IC50 value to convert. Must be a positive number.  
- **`unit`** (`str`):  
    The unit of the IC50 value. Supported units are:  
    - `"nM"` (nanomolar)  
    - `"µM"` (micromolar)  
    - `"mM"` (millimolar)  
    - `"M"` (molar)  

### Returns
- **`float`**:  
    The calculated pIC50 value.

### Raises
- **`ValueError`**:  
    Raised when:  
    - The IC50 value is not a positive number.  
    - An unsupported unit is provided.

### Example Usage

<!-- tabs:start -->

#### **Example 1**
```python
ic50_value = 50
unit = "nM"
pic50 = ic50_to_pic50(ic50_value, unit)
print(f"pIC50 for {ic50_value} {unit} is {pic50:.2f}")
```
**Expected Output:**
```
pIC50 for 50 nM is 7.30
```

#### **Example 2**
```python
ic50_value = 0.005
unit = "µM"
pic50 = ic50_to_pic50(ic50_value, unit)
print(f"pIC50 for {ic50_value} {unit} is {pic50:.2f}")
```
**Expected Output:**
```
pIC50 for 0.005 µM is 8.30
```

#### **Example 3**
```python
try:
    ic50_value = -5
    unit = "mM"
    pic50 = ic50_to_pic50(ic50_value, unit)
except ValueError as e:
    print(f"Error: {e}")
```
**Expected Output:**
```
Error: IC50 value must be a positive number.
```

#### **Example 4**
```python
try:
    ic50_value = 100
    unit = "invalid_unit"
    pic50 = ic50_to_pic50(ic50_value, unit)
except ValueError as e:
    print(f"Error: {e}")
```
**Expected Output:**
```
Error: Invalid unit 'invalid_unit'. Supported units are: nM, µM, mM, M.
```

<!-- tabs:end -->