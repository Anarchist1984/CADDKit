# Utils Functions

## Function: `ic50_to_pic50`

### Description
Converts an IC50 value to a pIC50 value based on the specified unit of measurement. The pIC50 value is a logarithmic measure used in pharmacology to indicate the potency of a compound in inhibiting a specific biological or biochemical function.

### Notes
- The function assumes that IC50 values are expressed in one of the supported units. Ensure accurate unit specification to avoid errors.
- The function uses base-10 logarithms for conversion.

### Supported Units and Conversion Factors
| Unit   | Conversion Factor to Molar (M) |
|--------|---------------------------------|
| `nM`   | `1e-9`                         |
| `µM`   | `1e-6`                         |
| `mM`   | `1e-3`                         |
| `M`    | `1`                            |

### Parameters
- **ic50** (`Union[float, int]`):  
  The IC50 value to be converted. Must be a positive number.
- **unit** (`str`):  
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
  - An invalid unit is provided.

### Example Usage

<!-- tabs:start -->

#### **Example 1**
**Example 1: Convert 50 nM IC50 to pIC50**
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
**Example 2: Convert 0.005 µM IC50 to pIC50**
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
**Example 3: Handle invalid IC50 value**
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
**Example 4: Handle invalid unit**
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
