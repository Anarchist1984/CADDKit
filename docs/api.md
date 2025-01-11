Here's a detailed Markdown documentation for the `caddkit.api.chembl` module, which includes descriptions, parameter details, return types, raised exceptions, and example usage for each function.

---

# `caddkit.api.chembl`

This module provides utility functions for querying data from the ChEMBL database, including targets, bioactivities, and compounds, based on UniProt IDs or ChEMBL IDs.

---

## **Function: `get_chembl_targets_by_uniprot`**

Retrieves target information from ChEMBL for a specified UniProt ID.

- **Parameters**:
  - `uniprot_id` (*str*): The UniProt ID for which target information is to be fetched.

- **Returns**:
  - `pd.DataFrame`: A DataFrame containing target information, including the fields:
    - `target_chembl_id`
    - `organism`
    - `pref_name`
    - `target_type`
    If no results are found or an error occurs, an empty DataFrame is returned.

- **Raises**:
  - `ValueError`: If no targets are found for the provided UniProt ID.
  - `TypeError`: If the provided UniProt ID is not a string.

- **Example**:
  ```python
  from caddkit.api.chembl import get_chembl_targets_by_uniprot

  targets_df = get_chembl_targets_by_uniprot("P12345")
  print(targets_df)
  ```

---

## **Function: `get_chembl_id_by_uniprot`**

Retrieves the ChEMBL ID for a target corresponding to a given UniProt ID.

- **Parameters**:
  - `uniprot_id` (*str*): The UniProt ID for which the ChEMBL ID is to be retrieved.
  - `loc` (*int*, optional): The index of the target in the results list to retrieve. Defaults to `0`.

- **Returns**:
  - `str`: The ChEMBL ID of the selected target.
  - `None`: If the specified index is out of bounds or an error occurs.

- **Raises**:
  - `IndexError`: If the specified index `loc` is out of bounds for the target results.
  - `KeyError`: If the `target_chembl_id` column is not found in the results DataFrame.

- **Example**:
  ```python
  from caddkit.api.chembl import get_chembl_id_by_uniprot

  chembl_id = get_chembl_id_by_uniprot("P12345")
  print(chembl_id)
  ```

---

## **Function: `query_chembl_bioactivity`**

Queries bioactivity data from ChEMBL for a given target ChEMBL ID.

- **Parameters**:
  - `chembl_id` (*str*): The ChEMBL ID of the target for which bioactivity data is to be queried.

- **Returns**:
  - `pd.DataFrame`: A DataFrame containing bioactivity data with the following columns:
    - `activity_id`
    - `assay_chembl_id`
    - `assay_description`
    - `assay_type`
    - `molecule_chembl_id`
    - `type`
    - `standard_units`
    - `relation`
    - `standard_value`
    - `target_chembl_id`
    - `target_organism`
    If no data is found or an error occurs, an empty DataFrame is returned.

- **Example**:
  ```python
  from caddkit.api.chembl import query_chembl_bioactivity

  bioactivity_df = query_chembl_bioactivity("CHEMBL12345")
  print(bioactivity_df)
  ```

---

## **Function: `query_chembl_compounds`**

Queries compound data from ChEMBL for a given list of molecule ChEMBL IDs.

- **Parameters**:
  - `compounds_list` (*list*): A list of molecule ChEMBL IDs to query.

- **Returns**:
  - `pd.DataFrame`: A DataFrame containing compound details with the following columns:
    - `molecule_chembl_id`
    - `molecule_structures`
    If an error occurs, an empty DataFrame is returned.

- **Example**:
  ```python
  from caddkit.api.chembl import query_chembl_compounds

  compound_list = ["CHEMBL123", "CHEMBL456"]
  compounds_df = query_chembl_compounds(compound_list)
  print(compounds_df)
  ```

---

## Example Workflow

```python
from caddkit.api.chembl import (
    get_chembl_targets_by_uniprot,
    get_chembl_id_by_uniprot,
    query_chembl_bioactivity,
    query_chembl_compounds,
)

# 1. Get targets for a UniProt ID
uniprot_id = "P12345"
targets_df = get_chembl_targets_by_uniprot(uniprot_id)

# 2. Retrieve the first ChEMBL ID
chembl_id = get_chembl_id_by_uniprot(uniprot_id)

# 3. Query bioactivity data
bioactivity_df = query_chembl_bioactivity(chembl_id)

# 4. Extract compound IDs and query compound data
compound_ids = bioactivity_df["molecule_chembl_id"].unique().tolist()
compounds_df = query_chembl_compounds(compound_ids)

# 5. Display results
print(targets_df)
print(bioactivity_df)
print(compounds_df)
```

---

This documentation format ensures clarity and consistency, including what exceptions each function might raise. Let me know if additional refinements are needed!