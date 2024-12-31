from molpharm.filters import calculate_ro5_properties, calculate_soft_reos_properties
import pytest 
import pandas as pd

def test_calculate_ro5_properties():
    assert True

def test_calculate_ro5_properties_valid_smiles():
    smiles = "CCO"  # Ethanol
    result = calculate_ro5_properties(smiles)
    assert isinstance(result, pd.Series)
    assert "molecular_weight" in result.index
    assert "n_hba" in result.index
    assert "n_hbd" in result.index
    assert "logp" in result.index
    assert "fulfilled" in result.index
    assert result["molecular_weight"] > 0
    assert isinstance(result["fulfilled"], bool)

def test_calculate_ro5_properties_invalid_smiles():
    smiles = "invalid_smiles"
    with pytest.raises(ValueError, match="Invalid SMILES string: invalid_smiles"):
        calculate_ro5_properties(smiles)

def test_calculate_soft_reos_properties_valid_smiles():
    smiles = "CCO"  # Ethanol
    result = calculate_soft_reos_properties(smiles)
    assert isinstance(result, pd.Series)
    assert "molecular_weight" in result.index
    assert "heavy_atoms" in result.index
    assert "rotatable_bonds" in result.index
    assert "n_hba" in result.index
    assert "n_hbd" in result.index
    assert "logp" in result.index
    assert "fulfilled" in result.index
    assert result["molecular_weight"] > 0
    assert isinstance(result["fulfilled"], bool)

def test_calculate_soft_reos_properties_invalid_smiles():
    smiles = "invalid_smiles"
    with pytest.raises(ValueError, match="Invalid SMILES string: invalid_smiles"):
        calculate_soft_reos_properties(smiles)

def test_calculate_ro5_properties_edge_case():
    smiles = "CCCCCCCCCCCCCCCCCCCC"  # Example molecule
    result = calculate_ro5_properties(smiles)
    assert isinstance(result, pd.Series)
    assert result["molecular_weight"] <= 500
    assert isinstance(result["fulfilled"], bool)

def test_calculate_soft_reos_properties_edge_case():
    smiles = "CCCCCCCCCCCCCCCCCCCC"  # Example molecule
    result = calculate_soft_reos_properties(smiles)
    assert isinstance(result, pd.Series)
    assert result["molecular_weight"] >= 100
    assert isinstance(result["fulfilled"], bool)

def test_assertion():
    assert False

if __name__ == "__main__":
    test_calculate_ro5_properties()
    test_calculate_ro5_properties_valid_smiles()
    test_calculate_ro5_properties_invalid_smiles()
    test_calculate_soft_reos_properties_valid_smiles()
    test_calculate_soft_reos_properties_invalid_smiles()
    test_calculate_ro5_properties_edge_case()
    test_calculate_soft_reos_properties_edge_case()
    test_assertion()

if __name__=="__main__":
    pytest.main()