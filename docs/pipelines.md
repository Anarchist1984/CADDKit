# ChEMBL Data Request Pipeline

The `caddkit.pipelines.chembl_data_request` module provides a pipeline for fetching, processing, and merging bioactivity and compound data from ChEMBL for a given UniProt ID. It is useful for preparing datasets for cheminformatics and drug discovery tasks.

---

## Class: `ChemblDataRequestPipeline`

### Description

A pipeline to automate the retrieval, processing, and merging of bioactivity and compound data from ChEMBL based on a specified UniProt ID.

---

### Initialization

#### `__init__(uniprot_id: str)`

Initializes the pipeline with the specified UniProt ID.

- **Parameters**:
  - `uniprot_id` (*str*): The UniProt ID of the target protein.

- **Raises**:
  - None.

- **Example**:
  ```python
  from caddkit.pipelines.chembl_data_request import ChemblDataRequestPipeline

  pipeline = ChemblDataRequestPipeline("P12345")
  ```

---

### Pipeline Steps

#### **1. Get ChEMBL ID**

##### `get_chembl_id() -> str`

Fetches the ChEMBL ID for the specified UniProt ID.

- **Returns**:
  - `chembl_id` (*str*): The ChEMBL ID of the target protein.

- **Raises**:
  - `RuntimeError`: If there is an error while fetching the ChEMBL ID.

- **Example**:
  ```python
  chembl_id = pipeline.get_chembl_id()
  print(chembl_id)
  ```

---

#### **2. Query Bioactivity Data**

##### `query_bioactivity_data(chembl_id: str) -> pd.DataFrame`

Fetches bioactivity data for a given ChEMBL ID.

- **Parameters**:
  - `chembl_id` (*str*): The ChEMBL ID for which to fetch bioactivity data.

- **Returns**:
  - `pd.DataFrame`: DataFrame containing raw bioactivity data.

- **Raises**:
  - `RuntimeError`: If there is an error while querying bioactivity data.

- **Example**:
  ```python
  bioactivity_data = pipeline.query_bioactivity_data("CHEMBL123456")
  print(bioactivity_data)
  ```

---

#### **3. Process Bioactivity Data**

##### `process_bioactivity_data(bioactivities_df: pd.DataFrame) -> pd.DataFrame`

Cleans and formats the bioactivity data.

- **Parameters**:
  - `bioactivities_df` (*pd.DataFrame*): Raw bioactivity data.

- **Returns**:
  - `pd.DataFrame`: Processed bioactivity data.

- **Raises**:
  - `RuntimeError`: If there is an error while processing bioactivity data.

- **Example**:
  ```python
  processed_bioactivity_data = pipeline.process_bioactivity_data(bioactivity_data)
  print(processed_bioactivity_data)
  ```

---

#### **4. Query Compound Data**

##### `query_compound_data(molecule_chembl_ids: list) -> pd.DataFrame`

Fetches compound data for a list of molecule ChEMBL IDs.

- **Parameters**:
  - `molecule_chembl_ids` (*list*): List of molecule ChEMBL IDs.

- **Returns**:
  - `pd.DataFrame`: DataFrame containing raw compound data.

- **Raises**:
  - `RuntimeError`: If there is an error while querying compound data.

- **Example**:
  ```python
  compound_data = pipeline.query_compound_data(["CHEMBL123", "CHEMBL456"])
  print(compound_data)
  ```

---

#### **5. Process Compound Data**

##### `process_compound_data(compounds_df: pd.DataFrame) -> pd.DataFrame`

Processes compound data to extract canonical SMILES and clean the data.

- **Parameters**:
  - `compounds_df` (*pd.DataFrame*): Raw compound data.

- **Returns**:
  - `pd.DataFrame`: Processed compound data with canonical SMILES.

- **Raises**:
  - `RuntimeError`: If there is an error while processing compound data.

- **Example**:
  ```python
  processed_compound_data = pipeline.process_compound_data(compound_data)
  print(processed_compound_data)
  ```

---

#### **6. Merge Bioactivity and Compound Data**

##### `merge_data(bioactivities_df: pd.DataFrame, compounds_df: pd.DataFrame) -> pd.DataFrame`

Merges processed bioactivity and compound data into a single DataFrame.

- **Parameters**:
  - `bioactivities_df` (*pd.DataFrame*): Processed bioactivity data.
  - `compounds_df` (*pd.DataFrame*): Processed compound data.

- **Returns**:
  - `pd.DataFrame`: Merged DataFrame containing bioactivity and compound data.

- **Raises**:
  - `RuntimeError`: If there is an error while merging data.

- **Example**:
  ```python
  merged_data = pipeline.merge_data(processed_bioactivity_data, processed_compound_data)
  print(merged_data)
  ```

---

#### **7. Convert IC50 to pIC50**

##### `convert_ic50_to_pic50(output_df: pd.DataFrame) -> pd.DataFrame`

Converts IC50 values to pIC50 and sorts the data by pIC50 values.

- **Parameters**:
  - `output_df` (*pd.DataFrame*): DataFrame containing IC50 values and units.

- **Returns**:
  - `pd.DataFrame`: DataFrame with pIC50 values sorted in descending order.

- **Raises**:
  - `RuntimeError`: If there is an error while converting IC50 to pIC50.

- **Example**:
  ```python
  final_data = pipeline.convert_ic50_to_pic50(merged_data)
  print(final_data)
  ```

---

### Run the Entire Pipeline

#### `run() -> pd.DataFrame`

Executes the full pipeline to retrieve, process, and merge ChEMBL data for the UniProt ID.

- **Returns**:
  - `pd.DataFrame`: Final processed DataFrame with canonical SMILES and pIC50 values.

- **Raises**:
  - `RuntimeError`: If there is an error at any stage of the pipeline.

- **Example**:
  ```python
  final_output = pipeline.run()
  print(final_output)
  ```

---

### Example Usage

```python
from caddkit.pipelines.chembl_data_request import ChemblDataRequestPipeline

# Initialize the pipeline with a UniProt ID
pipeline = ChemblDataRequestPipeline("P12345")

# Run the full pipeline
final_data = pipeline.run()

# Save the output to a CSV
final_data.to_csv("output_data.csv", index=False)
``` 