# APIs
# **caddkit.api.chembl**

## **Module Overview**
The `chembl.py` module provides functions for querying the ChEMBL database for target and bioactivity data, as well as retrieving compound information. It interacts with the ChEMBL API to fetch data based on UniProt IDs, ChEMBL IDs, and bioactivity details.

## **Functions**

### `get_chembl_targets_by_uniprot(uniprot_id: str) -> pd.DataFrame`
Retrieves target information from ChEMBL for a given UniProt ID.

**Parameters:**
- `uniprot_id` (str): The UniProt ID for which target information is to be fetched.

**Returns:**
- `pd.DataFrame`: A DataFrame containing target information such as 'target_chembl_id', 'organism', 'pref_name', and 'target_type'. If no results are found, an empty DataFrame is returned.

**Raises:**
- `ValueError`: If no targets are found for the provided UniProt ID.
- `TypeError`: If the provided UniProt ID is not a string.

**Example Usage:**
```python
targets_df = get_chembl_targets_by_uniprot("P12345")
```

---

### `get_chembl_id_by_uniprot(uniprot_id: str, loc: int = 0) -> Optional[str]`
Retrieves the ChEMBL ID for a target corresponding to a given UniProt ID.

**Parameters:**
- `uniprot_id` (str): The UniProt ID for which the ChEMBL ID is to be retrieved.
- `loc` (int, optional): The index of the target in the results list to retrieve. Defaults to 0.

**Returns:**
- `str`: The ChEMBL ID of the selected target.

**Raises:**
- `IndexError`: If the specified index `loc` is out of bounds for the target results.
- `KeyError`: If the 'target_chembl_id' column is not present in the results DataFrame.

**Example Usage:**
```python
chembl_id = get_chembl_id_by_uniprot("P12345")
```

---

### `query_chembl_bioactivity(chembl_id: str) -> pd.DataFrame`
Queries bioactivity data from ChEMBL for a given target ChEMBL ID.

**Parameters:**
- `chembl_id` (str): The ChEMBL ID of the target for which bioactivity data is to be queried.

**Returns:**
- `pd.DataFrame`: A DataFrame containing bioactivity data. If no data is found, an empty DataFrame is returned.

**Example Usage:**
```python
bioactivity_df = query_chembl_bioactivity("CHEMBL12345")
```

---

### `query_chembl_compounds(compounds_list: list) -> pd.DataFrame`
Queries compound data from ChEMBL for a given list of molecule ChEMBL IDs.

**Parameters:**
- `compounds_list` (list): A list of molecule ChEMBL IDs to query.

**Returns:**
- `pd.DataFrame`: A DataFrame containing the ChEMBL IDs and molecular structures of the compounds. If an error occurs, an empty DataFrame is returned.

**Example Usage:**
```python
compounds_df = query_chembl_compounds(["CHEMBL12345", "CHEMBL67890"])
```

---

# **caddkit.api.pdb**

## **Module Overview**
The `pdb.py` module provides functions for querying the RCSB PDB database, fetching PDB metadata, and retrieving ligand information for a given PDB ID. It allows for searching based on various criteria such as UniProt ID, experimental method, and ligand weight.

## **Functions**

### `create_query_by_uniprot_id(uniprot_id: str) -> rcsb.FieldQuery`
Generate a query to search by UniProt ID.

**Parameters:**
- `uniprot_id` (str): UniProt ID to search for.

**Returns:**
- `rcsb.FieldQuery`: The query object for the UniProt ID.

**Raises:**
- `ValueError`: If `uniprot_id` is not a valid non-empty string.

**Example Usage:**
```python
query = create_query_by_uniprot_id("P12345")
```

---

### `create_query_by_deposition_date(max_date: str) -> rcsb.FieldQuery`
Generate a query to search by deposition date.

**Parameters:**
- `max_date` (str): Maximum deposition date in 'YYYY-MM-DD' format.

**Returns:**
- `rcsb.FieldQuery`: The query object for the deposition date.

**Raises:**
- `ValueError`: If `max_date` is not a valid non-empty string.

**Example Usage:**
```python
query = create_query_by_deposition_date("2023-01-01")
```

---

### `create_query_by_experimental_method(method: str) -> rcsb.FieldQuery`
Generate a query to search by experimental method.

**Parameters:**
- `method` (str): Experimental method to search for.

**Returns:**
- `rcsb.FieldQuery`: The query object for the experimental method.

**Raises:**
- `ValueError`: If `method` is not a valid non-empty string.

**Example Usage:**
```python
query = create_query_by_experimental_method("X-ray diffraction")
```

---

### `create_query_by_resolution(max_resolution: float) -> rcsb.FieldQuery`
Generate a query to search by resolution.

**Parameters:**
- `max_resolution` (float): Maximum resolution.

**Returns:**
- `rcsb.FieldQuery`: The query object for resolution.

**Raises:**
- `ValueError`: If `max_resolution` is not a positive number.

**Example Usage:**
```python
query = create_query_by_resolution(2.0)
```

---

### `create_query_by_polymer_count(chain_count: int) -> rcsb.FieldQuery`
Generate a query to search by polymer chain count.

**Parameters:**
- `chain_count` (int): Number of polymer chains.

**Returns:**
- `rcsb.FieldQuery`: The query object for polymer chain count.

**Raises:**
- `ValueError`: If `chain_count` is not a non-negative integer.

**Example Usage:**
```python
query = create_query_by_polymer_count(2)
```

---

### `create_query_by_ligand_weight(min_weight: float) -> rcsb.FieldQuery`
Generate a query to search by ligand molecular weight.

**Parameters:**
- `min_weight` (float): Minimum ligand molecular weight.

**Returns:**
- `rcsb.FieldQuery`: The query object for ligand molecular weight.

**Raises:**
- `ValueError`: If `min_weight` is not a positive number.

**Example Usage:**
```python
query = create_query_by_ligand_weight(500.0)
```

---
### `search_rcsb_pdb(...) -> List[str]`
Search the RCSB PDB database using multiple criteria.

**Parameters:**
- `uniprot_id` (`Optional[str]`): UniProt ID to filter results by. Default is `None`.
- `max_deposition_date` (`Optional[str]`): Maximum deposition date in 'YYYY-MM-DD' format. Default is `None`.
- `experimental_method` (`Optional[str]`): Experimental method to filter results by (e.g., X-ray diffraction, NMR). Default is `None`.
- `max_resolution` (`Optional[float]`): Maximum resolution of the structure (in Angstroms). Default is `None`.
- `chain_count` (`Optional[int]`): Number of polymer chains to filter results by. Default is `None`.
- `min_ligand_weight` (`Optional[float]`): Minimum ligand molecular weight. Default is `None`.

**Returns:**
- `List[str]`: A list of matching PDB IDs.

**Raises:**
- `ValueError`: If no search criteria are provided.

**Example Usage:**
```python
pdb_ids = search_rcsb_pdb(uniprot_id="P12345", max_resolution=2.0)
```

---

### `fetch_pdb_metadata(pdb_id: str) -> Dict`
Retrieve metadata for a specific PDB ID with retries.

**Parameters:**
- `pdb_id` (str): PDB ID.

**Returns:**
- `Dict`: Metadata dictionary.

**Raises:**
- `ValueError`: If metadata retrieval fails.

**Example Usage:**
```python
metadata = fetch_pdb_metadata("1XYZ")
```

---

### `fetch_multiple_pdb_metadata(pdb_ids: List[str]) -> List[Dict]`
Retrieve metadata for multiple PDB IDs with retries.

**Parameters:**
- `pdb_ids` (List[str]): List of PDB IDs.

**Returns:**
- `List[Dict]`: List of metadata dictionaries.

**Example Usage:**
```python
metadata_list = fetch_multiple_pdb_metadata(["1XYZ", "2ABC"])
```

---

### `retrieve_ligand_data(pdb_id: str) -> Dict[str, Dict]`
Fetch ligand data for a given PDB ID.

**Parameters:**
- `pdb_id` (str): PDB ID.

**Returns:**
- `Dict[str, Dict]`: Ligand data mapped by ligand ID.

**Raises:**
- `requests.RequestException`: If fetching data fails.

**Example Usage:**
```python
ligand_data = retrieve_ligand_data("1XYZ")
```