# Fingerprint Calculation

```python
from caddkit import filters
```

### `calculate_morgan_fingerprint_as_bit_vect`
```python
calculate_morgan_fingerprint_as_bit_vect(smiles, radius=2, nBits=1024)
```
Calculates Morgan fingerprints for a given SMILES string.

#### Arguments
- **`smiles`** (`str`):  
  SMILES string for the compound.
- **`radius`** (`int`, optional):  
  Radius for the Morgan fingerprint (default is `2`).
- **`nBits`** (`int`, optional):  
  Length of the fingerprint vector (default is `1024`).

#### Returns
- **`np.array`**:  
  The computed Morgan fingerprint as a NumPy array. Returns a zero array if the SMILES string is invalid.

#### Raises
- **`ValueError`**:  
  If the SMILES string cannot be parsed into a molecule.

#### Example Usage
```python
fingerprint = calculate_morgan_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

### `calculate_ap_fingerprint_as_bit_vect`
```python
calculate_ap_fingerprint_as_bit_vect(smiles)
```
Calculates Atom Pair fingerprints for a given SMILES string.

#### Arguments
- **`smiles`** (`str`):  
  SMILES string for the compound.

#### Returns
- **`np.array`**:  
  The computed Atom Pair fingerprint as a NumPy array. Returns a zero array if the SMILES string is invalid.

#### Raises
- **`ValueError`**:  
  If the SMILES string cannot be parsed into a molecule.

#### Example Usage
```python
fingerprint = calculate_ap_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

### `calculate_rdk5_fingerprint_as_bit_vect`
```python
calculate_rdk5_fingerprint_as_bit_vect(smiles)
```
Calculates RDKit 5-bit hashed fingerprints for a given SMILES string.

#### Arguments
- **`smiles`** (`str`):  
  SMILES string for the compound.

#### Returns
- **`np.array`**:  
  The computed RDKit 5-bit hashed fingerprint as a NumPy array. Returns a zero array if the SMILES string is invalid.

#### Raises
- **`ValueError`**:  
  If the SMILES string cannot be parsed into a molecule.

#### Example Usage
```python
fingerprint = calculate_rdk5_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

### `calculate_maccs_fingerprint_as_bit_vect`
```python
calculate_maccs_fingerprint_as_bit_vect(smiles)
```
Calculates MACCS fingerprints for a given SMILES string.

#### Arguments
- **`smiles`** (`str`):  
  SMILES string for the compound.

#### Returns
- **`np.array`**:  
  The computed MACCS fingerprint as a NumPy array. Returns a zero array if the SMILES string is invalid.

#### Raises
- **`ValueError`**:  
  If the SMILES string cannot be parsed into a molecule.

#### Example Usage
```python
fingerprint = calculate_maccs_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

### `calculate_morgan2_fingerprint_as_bit_vect`
```python
calculate_morgan2_fingerprint_as_bit_vect(smiles, n_bits=2048)
```
Calculates Morgan fingerprints for a given SMILES string using a fixed radius of 2.

#### Arguments
- **`smiles`** (`str`):  
  SMILES string for the compound.
- **`n_bits`** (`int`, optional):  
  Number of bits for the fingerprint (default is `2048`).

#### Returns
- **`np.array`**:  
  The computed Morgan fingerprint as a NumPy array. Returns a zero array if the SMILES string is invalid.

#### Raises
- **`ValueError`**:  
  If the SMILES string cannot be parsed into a molecule.

#### Example Usage
```python
fingerprint = calculate_morgan2_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

### `calculate_morgan3_fingerprint_as_bit_vect`
```python
calculate_morgan3_fingerprint_as_bit_vect(smiles, n_bits=2048)
```
Calculates Morgan fingerprints for a given SMILES string using a fixed radius of 3.

#### Arguments
- **`smiles`** (`str`):  
  SMILES string for the compound.
- **`n_bits`** (`int`, optional):  
  Number of bits for the fingerprint (default is `2048`).

#### Returns
- **`np.array`**:  
  The computed Morgan fingerprint as a NumPy array. Returns a zero array if the SMILES string is invalid.

#### Raises
- **`ValueError`**:  
  If the SMILES string cannot be parsed into a molecule.

#### Example Usage
```python
fingerprint = calculate_morgan3_fingerprint_as_bit_vect("CCO")
print(fingerprint)
```

---

### `generate_fingerprint_dfs`
```python
generate_fingerprint_dfs(X_df, fingerprint_fn, smiles_col="smiles", fp_column_name="")
```
Generates a DataFrame with fingerprints for a given input DataFrame and fingerprint function, while retaining the original columns.

#### Arguments
- **`X_df`** (`pd.DataFrame`):  
  Input DataFrame containing at least a column specified by `smiles_col`.
- **`fingerprint_fn`** (`function`):  
  Function to calculate fingerprints from SMILES.
- **`smiles_col`** (`str`, optional):  
  Column name containing SMILES strings (default is `"smiles"`).
- **`fp_column_name`** (`str`, optional):  
  Prefix for fingerprint column names (default is `""`).

#### Returns
- **`pd.DataFrame`**:  
  DataFrame where each row corresponds to the original columns and the fingerprints of a compound.

#### Raises
- **`ValueError`**:  
  If the specified `smiles_col` is not in the input DataFrame.

#### Example Usage
```python
fingerprint_df = generate_fingerprint_dfs(X_df, calculate_morgan_fingerprint_as_bit_vect)
print(fingerprint_df)
```

---

### `generate_fingerprint_dfs_to_csv`
```python
generate_fingerprint_dfs_to_csv(X_df, fingerprint_fn, output_csv_path, smiles_col="smiles", fp_column_name="", chunk_size=100)
```
Generates fingerprints for a DataFrame and writes them incrementally into a CSV file, with error handling and progress tracking.

#### Arguments
- **`X_df`** (`pd.DataFrame`):  
  Input DataFrame containing at least a column specified by `smiles_col`.
- **`fingerprint_fn`** (`function`):  
  Function to calculate fingerprints from SMILES.
- **`output_csv_path`** (`str`):  
  Path to the output CSV file.
- **`smiles_col`** (`str`, optional):  
  Column name containing SMILES strings (default is `"smiles"`).
- **`fp_column_name`** (`str`, optional):  
  Prefix for fingerprint column names (default is `""`).
- **`chunk_size`** (`int`, optional):  
  Number of rows to process in each batch before writing to CSV (default is `100`).

#### Returns
- **`None`**  

#### Raises
- **`ValueError`**:  
  If the specified `smiles_col` is not in the input DataFrame.

#### Example Usage
```python
generate_fingerprint_dfs_to_csv(X_df, calculate_morgan_fingerprint_as_bit_vect, "output.csv")
```