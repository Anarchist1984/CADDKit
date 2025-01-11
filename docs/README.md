Here’s the updated release notes with the additional sections:

# Release Notes

## Version Information
- **Version**: 1.0.0-alpha.1.1
- **Release Date**: January 1, 2025

## New Features

### CHEMbl
- **`get_target_by_uniprot`**: Retrieves target information from ChEMBL by UniProt ID, returning details like `target_chembl_id`, `organism`, and `target_type`.
- **`get_chembl_id_by_uniprot`**: Fetches ChEMBL ID for a target using `get_target_by_uniprot`.
- **`query_bioactivity`**: Queries bioactivity data for a ChEMBL ID, focusing on IC50 values and binding assays.
- **`query_compounds`**: Queries compound data for ChEMBL IDs, returning molecular structures and related info.
- **`calculate_ro5_properties`**: Computes Lipinski's rule of five properties for a molecule (SMILES).
- **`calculate_soft_reos_properties`**: Calculates a softened version of the REOS criteria for a molecule (SMILES).

### PDB
- **`query_by_uniprot_id`**: Searches RCSB PDB by UniProt ID.
- **`query_by_deposition_date`**: Searches PDB for entries before a specific deposition date.
- **`query_by_experimental_method`**: Searches PDB by experimental method.
- **`query_by_resolution`**: Searches PDB by structure resolution.
- **`query_by_polymer_count`**: Searches PDB by polymer chain count.
- **`query_by_ligand_mw`**: Searches PDB by ligand molecular weight.
- **`search_pdb`**: Combines multiple search criteria to find matching PDB IDs.
- **`describe_one_pdb_id`**: Fetches metadata for a PDB ID with retry functionality.
- **`fetch_pdb_metadata`**: Fetches metadata for multiple PDB IDs.
- **`get_ligands`**: Retrieves ligand information for a given PDB ID.
- **`convert_ic50_to_pic50`**: Converts IC50 values (nM) to pIC50, returning NaN for invalid values.

### DataRequestPipeline
- A pipeline that fetches, processes, and merges bioactivity and compound data from ChEMBL for a UniProt ID, including:
  - Fetching ChEMBL ID, querying bioactivity and compound data, processing, merging, and converting IC50 values to pIC50.

### CompoundFilter
- A class to apply filters to a list of molecules (SMILES), including:
  - Adding filter functions, processing molecules through all filters, and categorizing them based on filter compliance. Returns separate DataFrames for passing and violating molecules.

## Breaking Changes
- No breaking changes in this release.

## Deprecations
- No deprecations in this release.

## Known Issues
- No known issues.

## Installation Instructions
- Ensure you are using Python 3.7 or later.
- Install or upgrade using pip:
  ```bash
  pip install caddkit
  ```

## Documentation
- **Coming soon**: Updated user and API documentation will be available shortly.

## Compatibility
- Compatible with the latest release of Python.