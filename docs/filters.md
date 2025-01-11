# Chemical Property Evaluation and Filtering

This module provides tools for evaluating chemical properties of molecules and applying various filtering criteria for drug discovery. It supports the implementation of chemical rules such as **Lipinski's Rule of Five** and **softened REOS (Rule of Five-like criteria)**. The module includes utility functions for evaluating individual molecules and a `CompoundFilter` class for batch processing.


## Functions

### `calculate_ro5_properties(smiles)`

Evaluates a molecule (SMILES) against **Lipinski's Rule of Five** criteria.

#### Parameters
- **`smiles`** (`str`): The SMILES representation of the molecule.

#### Returns
- **`pandas.Series`**:  
  Contains molecular weight, hydrogen bond donors/acceptors, logP, and compliance with the rule.

#### Raises
- **`ValueError`**: Raised if the input SMILES string is invalid.

#### Example
```python
from caddkit.filters import calculate_ro5_properties

result = calculate_ro5_properties("CCO")
print(result)
```
**Output:**
```
molecular_weight    46.041864
n_hba                1.000000
n_hbd                1.000000
logp                -0.001387
fulfilled            True
dtype: float64
```
---

### `calculate_soft_reos_properties(smiles)`

Evaluates a molecule (SMILES) against a **softened version of the REOS criteria**.

#### Parameters
- **`smiles`** (`str`): The SMILES representation of the molecule.

#### Returns
- **`pandas.Series`**:  
  Contains molecular weight, heavy atoms, rotatable bonds, hydrogen bond donors/acceptors, logP, and compliance with the criteria.

#### Raises
- **`ValueError`**: Raised if the input SMILES string is invalid.

#### Example
```python
from caddkit.filters import calculate_soft_reos_properties

result = calculate_soft_reos_properties("CCO")
print(result)
```
**Output:**
```
molecular_weight    46.041864
heavy_atoms          3.000000
rotatable_bonds      1.000000
n_hba                1.000000
n_hbd                1.000000
logp                -0.001387
fulfilled            True
dtype: float64
```

## Class: `CompoundFilter`

A class to apply multiple filtering rules to a dataset of molecules and track compliance.

### Methods

#### `add_filter(filter_func, name)`

Adds a filter function to the filter list.

- **`filter_func`** (`callable`): Function to evaluate compliance.
- **`name`** (`str`): Name of the filter for tracking violations.

#### Raises
- **`ValueError`**: If `filter_func` is not callable.
- **`TypeError`**: If `name` is not a string.

---

#### `filter(df, smiles_column)`

Processes a DataFrame of molecules against all added filters.

- **Parameters**:
  - **`df`** (`pandas.DataFrame`): DataFrame containing molecule data.
  - **`smiles_column`** (`str`): Column name with SMILES strings.

- **Returns**:
  - **`filtered_df`** (`pandas.DataFrame`): Molecules passing all filters.
  - **`violated_df`** (`pandas.DataFrame`): Molecules violating at least one filter with violation reasons.

- **Raises**:
  - **`KeyError`**: Raised if the `smiles_column` does not exist in the DataFrame.
  - **`Exception`**: Raised for any errors during filter function execution (e.g., invalid SMILES).

#### Example
```python
from caddkit.filters import CompoundFilter, calculate_ro5_properties

filter = CompoundFilter()
filter.add_filter(calculate_ro5_properties, "Lipinski's Rule of Five")

data = pd.DataFrame({"smiles": ["CCO", "CCCC"]})
filtered, violated = filter.filter(data, "smiles")

print("Filtered Molecules:\n", filtered)
print("Violated Molecules:\n", violated)
```
**Output:**
```
Filtered Molecules:
   smiles
0     CCO
Violated Molecules:
   smiles, violation_reason
0     CCO, Lipinski's Rule of Five
```

---

## Examples

### Evaluate a Single Molecule Against Lipinski's Rule of Five
```python
from caddkit.filters import calculate_ro5_properties

result = calculate_ro5_properties("CCO")
print(result)
```

---

### Batch Evaluation with `CompoundFilter`
```python
from caddkit.filters import CompoundFilter, calculate_ro5_properties

filter = CompoundFilter()
filter.add_filter(calculate_ro5_properties, "Lipinski's Rule of Five")

smiles_list = ["CCO", "CCCCC"]
data = pd.DataFrame({"smiles": smiles_list})

filtered, violated = filter.filter(data, "smiles")
print("Filtered Molecules:\n", filtered)
print("Violated Molecules:\n", violated)
```