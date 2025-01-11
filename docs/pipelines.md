# Pipelines
---
```python
from caddkit import pipelines
```
---

# Class: `ChemblDataRequestPipeline`

```python
pipeline = ChemblDataRequestPipeline(uniprot_id: str)
```

A pipeline for fetching, processing, and merging bioactivity and compound data from ChEMBL for a given UniProt ID. It automates data preparation for cheminformatics and drug discovery tasks.

## Initialization

### `__init__`
```python
__init__(uniprot_id: str)
```

Initializes the pipeline with a specified UniProt ID.

#### Arguments
- **`uniprot_id`** (`str`):  
    The UniProt ID of the target protein.

#### Raises
- **`ValueError`**: If the UniProt ID is invalid.

#### Example Usage
```python
from caddkit.pipelines.chembl_data_request import ChemblDataRequestPipeline

pipeline = ChemblDataRequestPipeline("P12345")
```

---

## Methods

### `get_chembl_id`
```python
get_chembl_id() -> str
```

Fetches the ChEMBL ID for the specified UniProt ID.

#### Returns
- **`str`**: The ChEMBL ID of the target protein.

#### Raises
- **`RuntimeError`**: If fetching the ChEMBL ID fails.

#### Example Usage
```python
chembl_id = pipeline.get_chembl_id()
print(chembl_id)
```

---

### `query_bioactivity_data`
```python
query_bioactivity_data(chembl_id: str) -> pd.DataFrame
```

Fetches bioactivity data for a given ChEMBL ID.

#### Arguments
- **`chembl_id`** (`str`):  
    The ChEMBL ID to fetch bioactivity data for.

#### Returns
- **`pd.DataFrame`**: DataFrame containing raw bioactivity data.

#### Raises
- **`RuntimeError`**: If querying bioactivity data fails.

#### Example Usage
```python
bioactivity_data = pipeline.query_bioactivity_data("CHEMBL123456")
print(bioactivity_data)
```

---

### `process_bioactivity_data`
```python
process_bioactivity_data(bioactivities_df: pd.DataFrame) -> pd.DataFrame
```

Cleans and formats the bioactivity data.

#### Arguments
- **`bioactivities_df`** (`pd.DataFrame`):  
    Raw bioactivity data.

#### Returns
- **`pd.DataFrame`**: Processed bioactivity data.

#### Raises
- **`RuntimeError`**: If processing fails.

#### Example Usage
```python
processed_data = pipeline.process_bioactivity_data(bioactivity_data)
print(processed_data)
```

---

### `query_compound_data`
```python
query_compound_data(molecule_chembl_ids: list) -> pd.DataFrame
```

Fetches compound data for a list of molecule ChEMBL IDs.

#### Arguments
- **`molecule_chembl_ids`** (`list`):  
    List of molecule ChEMBL IDs.

#### Returns
- **`pd.DataFrame`**: DataFrame containing raw compound data.

#### Raises
- **`RuntimeError`**: If querying compound data fails.

#### Example Usage
```python
compound_data = pipeline.query_compound_data(["CHEMBL123", "CHEMBL456"])
print(compound_data)
```

---

### `process_compound_data`
```python
process_compound_data(compounds_df: pd.DataFrame) -> pd.DataFrame
```

Processes compound data to extract canonical SMILES and clean the data.

#### Arguments
- **`compounds_df`** (`pd.DataFrame`):  
    Raw compound data.

#### Returns
- **`pd.DataFrame`**: Processed compound data with canonical SMILES.

#### Raises
- **`RuntimeError`**: If processing fails.

#### Example Usage
```python
processed_compound_data = pipeline.process_compound_data(compound_data)
print(processed_compound_data)
```

---

### `merge_data`
```python
merge_data(bioactivities_df: pd.DataFrame, compounds_df: pd.DataFrame) -> pd.DataFrame
```

Merges processed bioactivity and compound data into a single DataFrame.

#### Arguments
- **`bioactivities_df`** (`pd.DataFrame`):  
    Processed bioactivity data.  
- **`compounds_df`** (`pd.DataFrame`):  
    Processed compound data.

#### Returns
- **`pd.DataFrame`**: Merged DataFrame containing bioactivity and compound data.

#### Raises
- **`RuntimeError`**: If merging data fails.

#### Example Usage
```python
merged_data = pipeline.merge_data(processed_bioactivity_data, processed_compound_data)
print(merged_data)
```

---

### `convert_ic50_to_pic50`
```python
convert_ic50_to_pic50(output_df: pd.DataFrame) -> pd.DataFrame
```

Converts IC50 values to pIC50 and sorts the data by pIC50.

#### Arguments
- **`output_df`** (`pd.DataFrame`):  
    DataFrame containing IC50 values and units.

#### Returns
- **`pd.DataFrame`**: DataFrame with pIC50 values sorted in descending order.

#### Raises
- **`RuntimeError`**: If conversion fails.

#### Example Usage
```python
final_data = pipeline.convert_ic50_to_pic50(merged_data)
print(final_data)
```

---

### `run`
```python
run() -> pd.DataFrame
```

Executes the entire pipeline to retrieve, process, and merge ChEMBL data for the specified UniProt ID.

#### Returns
- **`pd.DataFrame`**: Final processed DataFrame with canonical SMILES and pIC50 values.

#### Raises
- **`RuntimeError`**: If any pipeline step fails.

#### Example Usage
```python
final_output = pipeline.run()
print(final_output)
```

---

## Full Pipeline Example

```python
from caddkit.pipelines.chembl_data_request import ChemblDataRequestPipeline

pipeline = ChemblDataRequestPipeline("P12345")
final_data = pipeline.run()
final_data.to_csv("output_data.csv", index=False)
```