from molpharm.chembl import get_chembl_id, get_target_by_uniprot

def test_get_chembl_id():
    # Test case for a valid UniProt ID
    uniprot_id = 'P00533'
    chembl_id = get_chembl_id(uniprot_id)
    assert chembl_id == 'CHEMBL203'

    # Test case for an invalid UniProt ID
    uniprot_id = 'INVALID'
    chembl_id = get_chembl_id(uniprot_id)
    assert chembl_id is None

def test_get_target_by_uniprot():
    # Test case for a valid UniProt ID
    uniprot_id = 'P00533'
    targets_df = get_target_by_uniprot(uniprot_id)
    assert not targets_df.empty

    # Test case for an invalid UniProt ID
    uniprot_id = 'INVALID'
    targets_df = get_target_by_uniprot(uniprot_id)
    assert targets_df.empty