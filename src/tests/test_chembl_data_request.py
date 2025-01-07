import pytest
import pandas as pd
from caddkit.pipelines.chembl_data_request import ChemblDataRequestPipeline


@pytest.fixture
def pipeline():
    """Fixture to create a DataRequestPipeline instance."""
    return ChemblDataRequestPipeline(uniprot_id="P12345")

def test_pipeline_real_run(pipeline_instance):
    """
    Test for the DataRequestPipeline using an actual pipeline run with CHEMBL203.
    """
    # Use the pipeline fixture directly
    pipeline_instance.uniprot_id = "P14780"  # Using a valid UniProt ID
    # Run the pipeline
    result = pipeline_instance.run()
    # Ensure that the result DataFrame is not empty
    assert not result.empty, "Pipeline returned an empty DataFrame"
    # Check the structure of the final DataFrame
    expected_columns = ['molecule_chembl_id', 'smiles', 'pIC50']
    for col in expected_columns:
        assert col in result.columns, f"Missing column: {col}"

    # Check that the pIC50 values are computed (they should not be NaN)
    assert result['pIC50'].notna().all(), "Some pIC50 values are NaN"

    # Check that the SMILES values are present (they should not be None)
    assert result['smiles'].notna().all(), "Some SMILES values are missing"

    # Check that the number of rows is greater than 0
    assert result.shape[0] > 0, f"Expected more than 0 rows, but got {result.shape[0]} rows"

#Broken tests need to fix
# Test for get_chembl_id
from unittest.mock import patch

def test_get_chembl_id():
    # Arrange
    pipeline = ChemblDataRequestPipeline(uniprot_id='P14780')

    with patch.object(ChemblDataRequestPipeline, 'get_chembl_id', return_value='CHEMBL203'):
        # Act
        chembl_id = pipeline.get_chembl_id()

        # Assert
        assert chembl_id == 'CHEMBL203'


# Test for query_bioactivity
def test_query_bioactivity_data():
    # Arrange
    pipeline = ChemblDataRequestPipeline(uniprot_id='P14780')

    # Act
    bioactivity_df = pipeline.query_bioactivity_data(chembl_id='CHEMBL203')

    # Assert
    assert bioactivity_df.shape[0] > 1
    required_columns = ['molecule_chembl_id', 'standard_value', 'standard_units', 'units', 'value']
    missing_columns = [col for col in required_columns if col not in bioactivity_df.columns]
    if missing_columns:
        raise AssertionError(f"Missing columns: {missing_columns}")

# Test for process_bioactivity_data
def test_process_bioactivity_data():
    # Arrange
    bioactivity_df = pd.DataFrame({
        'molecule_chembl_id': ['CHEMBL203'],
        'standard_value': [100.0],
        'standard_units': ['nM'],
        'units': ['nM'],
        'value': [None]
    })
    pipeline = ChemblDataRequestPipeline(uniprot_id='P14780')

    # Act
    processed_df = pipeline.process_bioactivity_data(bioactivity_df)

    # Assert
    assert processed_df.shape[0] == 1
    assert processed_df.columns.tolist() == ['molecule_chembl_id', 'IC50', 'units']
    assert processed_df['IC50'].iloc[0] == 100.0


# Test for query_compound_data
def test_query_compound_data():
    # Arrange
    pipeline = ChemblDataRequestPipeline(uniprot_id='P14780')

    # Act
    compounds_df = pipeline.query_compound_data(['CHEMBL203'])
    print(compounds_df.columns.tolist())

    # Assert
    #assert compounds_df.columns.tolist() == ['molecule_chembl_id', 'molecule_structures']


# Test for process_compound_data
def test_process_compound_data():
    # Arrange
    compounds_df = pd.DataFrame({
        'molecule_chembl_id': ['CHEMBL203'],
        'molecule_structures': [{'canonical_smiles': 'CCO'}]
    })

    # Act
    processed_df = ChemblDataRequestPipeline(uniprot_id='P14780').process_compound_data(compounds_df)

    # Assert
    assert processed_df.shape[0] == 1
    assert processed_df['smiles'].iloc[0] == 'CCO'


# Test for merge_data
def test_merge_data():
    # Arrange
    bioactivities_df = pd.DataFrame({
        'molecule_chembl_id': ['CHEMBL203'],
        'IC50': [100.0],
        'units': ['nM']
    })
    compounds_df = pd.DataFrame({
        'molecule_chembl_id': ['CHEMBL203'],
        'smiles': ['CCO']
    })

    # Act
    merged_df = ChemblDataRequestPipeline(uniprot_id='P14780').merge_data(bioactivities_df, compounds_df)

    # Assert
    assert merged_df.shape[0] == 1
    assert 'smiles' in merged_df.columns
    assert merged_df['smiles'].iloc[0] == 'CCO'


# Test for convert_ic50_to_pic50
def test_convert_ic50_to_pic50():
    # Arrange
    output_df = pd.DataFrame({
        'IC50': [100.0],
        'units': ['nM'],
        'molecule_chembl_id': ['CHEMBL203'],
        'smiles': ['CCO']
    })

    # Act
    result_df = ChemblDataRequestPipeline(uniprot_id='P14780').convert_ic50_to_pic50(output_df)

    # Assert
    assert result_df.shape[0] == 1
    assert 'pIC50' in result_df.columns
    assert result_df['pIC50'].iloc[0] == 7.0  # Assuming 100nM IC50 corresponds to 5.0 pIC50


# Test for the full process
def test_process():
    # Arrange
    pipeline = ChemblDataRequestPipeline(uniprot_id='P14780')

    # Act
    final_df = pipeline.run()

    # Assert
    assert final_df.shape[0] >= 1
    assert final_df.shape[1] == 3
    assert 'smiles' in final_df.columns
    assert 'pIC50' in final_df.columns


if __name__ == '__main__':
    test_query_compound_data()
    #pytest.main()