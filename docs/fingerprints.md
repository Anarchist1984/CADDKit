# Fingerprints Module

This module provides functionality for generating molecular fingerprints from SMILES representations. Fingerprints are essential for comparing molecules in cheminformatics tasks such as similarity searches and machine learning. This module supports various types of fingerprints, including **Morgan**, **Atom Pair (AP)**, **RDKit 5-bit**, and **MACCS** fingerprints. It also includes functions for generating fingerprints in bulk and saving the results to a CSV file.

---

## Morgan Fingerprints

```
calculate_morgan_fingerprint_as_bit_vect(smiles, radius=2, nBits=1024)
```

Calculates the Morgan fingerprint for a given SMILES string.

#### Parameters
- **`smiles`** (`str`): The SMILES string representing the compound.
- **`radius`** (`int`): The radius for the Morgan fingerprint (default is 2).
- **`nBits`** (`int`): The length of the fingerprint vector (default is 1024).

#### Returns
- **`np.array`**: The computed Morgan fingerprint as a NumPy array.

#### Example
```python
from caddkit.fingerprints import calculate_morgan_fingerprint_as_bit_vect

fingerprint = calculate_morgan_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

## Atom Pair (AP) Fingerprints

```
calculate_ap_fingerprint_as_bit_vect(smiles)
```

Calculates the Atom Pair (AP) fingerprint for a given SMILES string.

#### Parameters
- **`smiles`** (`str`): The SMILES string representing the compound.

#### Returns
- **`np.array`**: The computed Atom Pair fingerprint as a NumPy array.

#### Example
```python
from caddkit.fingerprints import calculate_ap_fingerprint_as_bit_vect

fingerprint = calculate_ap_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

## RDKit 5-bit Fingerprints

```
calculate_rdk5_fingerprint_as_bit_vect(smiles)
```

Calculates the RDKit 5-bit hashed fingerprint for a given SMILES string.

#### Parameters
- **`smiles`** (`str`): The SMILES string representing the compound.

#### Returns
- **`np.array`**: The computed RDKit 5-bit hashed fingerprint as a NumPy array.

#### Example
```python
from caddkit.fingerprints import calculate_rdk5_fingerprint_as_bit_vect

fingerprint = calculate_rdk5_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

## MACCS Fingerprints

```
calculate_maccs_fingerprint_as_bit_vect(smiles)
```

Calculates the MACCS fingerprint for a given SMILES string.

#### Parameters
- **`smiles`** (`str`): The SMILES string representing the compound.

#### Returns
- **`np.array`**: The computed MACCS fingerprint as a NumPy array.

#### Example
```python
from caddkit.fingerprints import calculate_maccs_fingerprint_as_bit_vect

fingerprint = calculate_maccs_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

## Morgan2 Fingerprints (Radius 2)

```
calculate_morgan2_fingerprint_as_bit_vect(smiles, n_bits=2048)
```

Calculates the Morgan fingerprint with radius 2 for a given SMILES string.

#### Parameters
- **`smiles`** (`str`): The SMILES string representing the compound.
- **`n_bits`** (`int`): The length of the fingerprint vector (default is 2048).

#### Returns
- **`np.array`**: The computed Morgan fingerprint as a NumPy array.

#### Example
```python
from caddkit.fingerprints import calculate_morgan2_fingerprint_as_bit_vect

fingerprint = calculate_morgan2_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

## Morgan3 Fingerprints (Radius 3)

```
calculate_morgan3_fingerprint_as_bit_vect(smiles, n_bits=2048)
```

Calculates the Morgan fingerprint with radius 3 for a given SMILES string.

#### Parameters
- **`smiles`** (`str`): The SMILES string representing the compound.
- **`n_bits`** (`int`): The length of the fingerprint vector (default is 2048).

#### Returns
- **`np.array`**: The computed Morgan fingerprint as a NumPy array.

#### Example
```python
from caddkit.fingerprints import calculate_morgan3_fingerprint_as_bit_vect

fingerprint = calculate_morgan3_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

## Bulk Fingerprint Generation

```
generate_fingerprint_dfs(X_df, fingerprint_fn, smiles_col="smiles", fp_column_name="")
```

Generates a DataFrame of fingerprints for a given DataFrame and fingerprint function.

#### Parameters
- **`X_df`** (`pd.DataFrame`): Input DataFrame containing at least the specified `smiles_col`.
- **`fingerprint_fn`** (`function`): Function to calculate fingerprints from SMILES.
- **`smiles_col`** (`str`): Column name containing SMILES strings (default is `"smiles"`).
- **`fp_column_name`** (`str`): Prefix for fingerprint column names.

#### Returns
- **`pd.DataFrame`**: A DataFrame with original columns and calculated fingerprints.

#### Raises
- **`ValueError`**: Raised if the specified `smiles_col` is not in the DataFrame.

#### Example
```python
import pandas as pd
from caddkit.fingerprints import generate_fingerprint_dfs, calculate_morgan_fingerprint_as_bit_vect

df = pd.DataFrame({"smiles": ["CCO", "CCN"]})
result_df = generate_fingerprint_dfs(df, calculate_morgan_fingerprint_as_bit_vect)
print(result_df)
```

---

### To CSV

```
generate_fingerprint_dfs_to_csv(X_df, fingerprint_fn, output_csv_path, smiles_col="smiles", fp_column_name="" chunk_size=100)
```

Generates fingerprints for a DataFrame and writes them to a CSV file incrementally.

#### Parameters
- **`X_df`** (`pd.DataFrame`): Input DataFrame containing at least the specified `smiles_col`.
- **`fingerprint_fn`** (`function`): Function to calculate fingerprints from SMILES.
- **`output_csv_path`** (`str`): Path to the output CSV file.
- **`smiles_col`** (`str`): Column name containing SMILES strings (default is `"smiles"`).
- **`fp_column_name`** (`str`): Prefix for fingerprint column names.
- **`chunk_size`** (`int`): Number of rows to process in each batch (default is 100).

#### Returns
- **`None`**: Writes fingerprints to a CSV file.

#### Raises
- **`ValueError`**: Raised if the specified `smiles_col` is not in the DataFrame.

#### Example
```python
import pandas as pd
from caddkit.fingerprints import generate_fingerprint_dfs_to_csv, calculate_morgan_fingerprint_as_bit_vect

df = pd.DataFrame({"smiles": ["CCO", "CCN"]})
generate_fingerprint_dfs_to_csv(df, calculate_morgan_fingerprint_as_bit_vect, "fingerprints.csv")
```