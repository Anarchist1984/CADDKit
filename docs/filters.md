# Filtering
---
## Functions
### `calculate_ro5_properties`

Tests if the input molecule (SMILES) fulfills Lipinski's rule of five (Ro5).

#### Parameters
- `smiles` (str): SMILES representation of the molecule.

#### Returns
- `pandas.Series`: A series containing the following properties:
    - `molecular_weight`: Molecular weight of the molecule.
    - `n_hba`: Number of hydrogen bond acceptors.
    - `n_hbd`: Number of hydrogen bond donors.
    - `logp`: LogP (octanol-water partition coefficient).
    - `fulfilled`: Boolean indicating whether the molecule fulfills at least 3 of the 4 Lipinski criteria.

#### Raises
- `ValueError`: If the SMILES string is invalid (cannot be converted to a molecule).

---

### `calculate_soft_reos_properties`

Tests if the input molecule (SMILES) fulfills a softened version of the REOS criteria.

#### Parameters
- `smiles` (str): SMILES representation of the molecule.

#### Returns
- `pandas.Series`: A series containing the following properties:
    - `molecular_weight`: Molecular weight of the molecule.
    - `heavy_atoms`: Number of heavy atoms (non-hydrogen atoms).
    - `rotatable_bonds`: Number of rotatable bonds in the molecule.
    - `n_hba`: Number of hydrogen bond acceptors.
    - `n_hbd`: Number of hydrogen bond donors.
    - `logp`: LogP (octanol-water partition coefficient).
    - `fulfilled`: Boolean indicating whether the molecule satisfies all REOS criteria.

#### Raises
- `ValueError`: If the SMILES string is invalid (cannot be converted to a molecule).

---
# Classes

## `CompoundFilter`

A class to apply multiple filters to a dataset of molecules represented by SMILES strings.

#### Attributes
- `filters`: A list of filter functions that take a SMILES string as input and return a pandas Series containing measurements and a `fulfilled` boolean.
- `filter_names`: A list of strings representing the names of the filters, used for tracking violations.

### Methods

#### `__init__`

Initializes the `CompoundFilter` object with empty filter and filter name lists.

---

#### `add_filter`

Adds a filter function to the filter list.

###### Parameters
- `filter_func` (callable): A function that takes a SMILES string as input and returns a pandas Series containing measurements and a `fulfilled` boolean.
- `name` (str): Name of the filter for tracking violations.

###### Raises
- `ValueError`: If `filter_func` is not callable.
- `TypeError`: If `name` is not a string.

---

#### `filter`

Processes a DataFrame of molecules through all added filters.

###### Parameters
- `df` (pandas.DataFrame): DataFrame containing molecule data, including a column with SMILES strings.
- `smiles_column` (str): The column name containing SMILES strings.

###### Returns
- `filtered_df` (pandas.DataFrame): DataFrame of molecules that passed all filters, retaining all original columns.
- `violated_df` (pandas.DataFrame): DataFrame of molecules that violated at least one filter, retaining all original columns and adding a column for violation reasons.

###### Raises
- `KeyError`: If `smiles_column` does not exist in the DataFrame.