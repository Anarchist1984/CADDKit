from molpharm.chembl import get_chembl_id, get_target_by_uniprot, query_bioactivity
import pandas as pd

def test_get_chembl_id():
    # Test case for a valid UniProt ID
    uniprot_id = 'P14780'
    chembl_id = get_chembl_id(uniprot_id)
    assert chembl_id == 'CHEMBL321'

    # Test case for an invalid UniProt ID
    uniprot_id = 'INVALID'
    chembl_id = get_chembl_id(uniprot_id)
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
    #This is broken, IDK why
    chembl_id = "CHEMBL203"
    bioactivity = query_bioactivity(chembl_id)
    
    assert bioactivity.iloc[0]['activity_id'] == 33892
    assert bioactivity.iloc[0]['assay_chembl_id'] == 'CHEMBL715225'
    assert bioactivity.iloc[0]['assay_description'] == 'In vitro inhibitory activity against matrix metalloproteinase 9 (MMP9)'
    assert bioactivity.iloc[0]['assay_type'] == 'B'
    assert bioactivity.iloc[0]['molecule_chembl_id'] == 'CHEMBL80814'
    assert bioactivity.iloc[0]['relation'] == '='
    assert bioactivity.iloc[0]['standard_units'] == 'nM'
    assert bioactivity.iloc[0]['standard_value'] == 34.0
    assert bioactivity.iloc[0]['target_chembl_id'] == 'CHEMBL321'
    assert bioactivity.iloc[0]['target_organism'] == 'Homo sapiens'
    assert bioactivity.iloc[0]['type'] == 'IC50'
    assert bioactivity.iloc[0]['units'] == 'nM'
    assert bioactivity.iloc[0]['value'] == 34.0
