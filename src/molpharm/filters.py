import pandas as pd
from rdkit.Chem import Descriptors
from rdkit import Chem

def calculate_ro5_properties(smiles):
    """
    Test if input molecule (SMILES) fulfills Lipinski's rule of five.

    Parameters
    ----------
    smiles : str
        SMILES for a molecule.

    Returns
    -------
    pandas.Series
        Molecular weight, number of hydrogen bond acceptors/donor and logP value
        and Lipinski's rule of five compliance for input molecule.
    """
    # RDKit molecule from SMILES
    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")
    # Calculate Ro5-relevant chemical properties
    molecular_weight = Descriptors.ExactMolWt(molecule)
    n_hba = Descriptors.NumHAcceptors(molecule)
    n_hbd = Descriptors.NumHDonors(molecule)
    logp = Descriptors.MolLogP(molecule)
    # Check if Ro5 conditions fulfilled
    conditions = [molecular_weight <= 500, n_hba <= 10, n_hbd <= 5, logp <= 5]
    ro5_fulfilled = sum(conditions) >= 3
    # Return True if no more than one out of four conditions is violated
    return pd.Series(
        [molecular_weight, n_hba, n_hbd, logp, ro5_fulfilled],
        index=["molecular_weight", "n_hba", "n_hbd", "logp", "fulfilled"]
    )

def calculate_soft_reos_properties(smiles):
    """
    Test if input molecule (SMILES) fulfills a softened version of the REOS criteria.

    Parameters
    ----------
    smiles : str
        SMILES for a molecule.

    Returns
    -------
    pandas.Series
        Molecular weight, number of heavy atoms, number of rotatable bonds,
        hydrogen-bond donors/acceptors, logP value, and REOS compliance for the input molecule.
    """
    # RDKit molecule from SMILES
    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")
    # Calculate REOS-relevant chemical properties
    molecular_weight = Descriptors.ExactMolWt(molecule)
    n_heavy_atoms = Descriptors.HeavyAtomCount(molecule)  # Heavy atoms (non-hydrogen)
    n_rotatable_bonds = Descriptors.NumRotatableBonds(molecule)
    n_hba = Descriptors.NumHAcceptors(molecule)
    n_hbd = Descriptors.NumHDonors(molecule)
    logp = Descriptors.MolLogP(molecule)

    # Define REOS criteria (softened)
    conditions = [
        100 <= molecular_weight <= 700,  # Molecular weight between 100 and 700 g/mol
        5 <= n_heavy_atoms <= 50,        # Number of heavy atoms between 5 and 50
        0 <= n_rotatable_bonds <= 12,    # Number of rotatable bonds between 0 and 12
        0 <= n_hbd <= 5,                 # Hydrogen bond donors between 0 and 5
        0 <= n_hba <= 10,                # Hydrogen bond acceptors between 0 and 10
        -5 < logp < 7.5                  # Hydrophobicity (logP) between -5 and 7.5
    ]

    # Check if all conditions are satisfied
    reos_fulfilled = all(conditions)

    # Return the results in a pandas Series
    return pd.Series(
        [molecular_weight, n_heavy_atoms, n_rotatable_bonds, n_hba, n_hbd, logp, reos_fulfilled],
        index=["molecular_weight", "heavy_atoms", "rotatable_bonds", "n_hba", "n_hbd", "logp", "fulfilled"]
    )