from molpharm.chembl import get_chembl_id_by_uniprot, get_target_by_uniprot, query_bioactivity
import pytest

def test_get_chembl_id():
    # Test case for a valid UniProt ID
    uniprot_id = 'P14780'
    chembl_id = get_chembl_id_by_uniprot(uniprot_id)
    assert chembl_id == 'CHEMBL321'

    # Test case for an invalid UniProt ID
    uniprot_id = 'INVALID'
    chembl_id = get_chembl_id_by_uniprot(uniprot_id)
    assert chembl_id is None

def test_get_target_by_uniprot():
    # Test case for a valid UniProt ID
    uniprot_id = 'P14780'
    targets_df = get_target_by_uniprot(uniprot_id)
    assert not targets_df.empty
    assert targets_df.iloc[0]['organism'] == 'Homo sapiens'
    assert targets_df.iloc[0]['pref_name'] == 'Matrix metalloproteinase 9'
    assert targets_df.iloc[0]['target_chembl_id'] == 'CHEMBL321'
    assert targets_df.iloc[0]['target_type'] == 'SINGLE PROTEIN'

    # Test case for an invalid UniProt ID
    uniprot_id = 'INVALID'
    targets_df = get_target_by_uniprot(uniprot_id)
    assert targets_df.empty

def test_query_bioactivity():
    # Test to ensure that bioactivity data returned is correct for a given ChemBL ID
    chembl_id = "CHEMBL203"
    bioactivity = query_bioactivity(chembl_id)
    
    # Check that the first row contains the expected values
    assert bioactivity.shape[0] > 0, "Bioactivity data is empty"
    
    # Check that all the expected fields exist and contain the correct data
    assert 'activity_id' in bioactivity.columns, "Missing 'activity_id' column"
    assert 'assay_chembl_id' in bioactivity.columns, "Missing 'assay_chembl_id' column"
    assert 'assay_description' in bioactivity.columns, "Missing 'assay_description' column"
    assert 'assay_type' in bioactivity.columns, "Missing 'assay_type' column"
    assert 'molecule_chembl_id' in bioactivity.columns, "Missing 'molecule_chembl_id' column"
    assert 'relation' in bioactivity.columns, "Missing 'relation' column"
    assert 'standard_units' in bioactivity.columns, "Missing 'standard_units' column"
    assert 'standard_value' in bioactivity.columns, "Missing 'standard_value' column"
    assert 'target_chembl_id' in bioactivity.columns, "Missing 'target_chembl_id' column"
    assert 'target_organism' in bioactivity.columns, "Missing 'target_organism' column"
    assert 'type' in bioactivity.columns, "Missing 'type' column"
    assert 'units' in bioactivity.columns, "Missing 'units' column"
    assert 'value' in bioactivity.columns, "Missing 'value' column"

if __name__ == "__main__":
    pytest.main()
