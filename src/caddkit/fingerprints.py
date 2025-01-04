from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
import numpy as np
import pandas as pd

def calculate_morgan_fingerprint_as_bit_vect(smiles, radius=2, nBits=1024):
    """
    Calculate Morgan fingerprints for a given SMILES string.
    Args:
        smiles (str): SMILES string for the compound.
        radius (int): Radius for the Morgan fingerprint.
        nBits (int): Length of the fingerprint vector.

    Returns:
        np.array: The computed Morgan fingerprint or zeros if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
        arr = np.zeros((0,), dtype=np.int8)
        DataStructs.ConvertToNumpyArray(fp,arr)
        return arr
    else:
        return np.zeros(nBits, dtype=np.float32)


def calculate_ap_fingerprint_as_bit_vect(smiles):
    """
    Calculate Atom Pair fingerprints for a given SMILES string.
    Args:
        smiles (str): SMILES string for the compound.

    Returns:
        np.array: The computed AP fingerprint or zeros if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fp = AllChem.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=2048)
        arr = np.zeros((0,), dtype=np.int8)
        DataStructs.ConvertToNumpyArray(fp,arr)
        return arr
    else:
        return np.zeros(2048, dtype=np.float32)


def calculate_rdk5_fingerprint_as_bit_vect(smiles):
    """
    Calculate RDKit 5-bit hashed fingerprints for a given SMILES string.
    Args:
        smiles (str): SMILES string for the compound.

    Returns:
        np.array: The computed RDKit 5-bit hashed fingerprint or zeros if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fp = Chem.RDKFingerprint(mol)
        arr = np.zeros((0,), dtype=np.int8)
        DataStructs.ConvertToNumpyArray(fp,arr)
        return arr
    else:
        return np.zeros(2048, dtype=np.float32)
        
def generate_fingerprint_dfs(X_df, fingerprint_fn, fingerprint_name):
    """
    Generate a DataFrame with fingerprints for a given input DataFrame and fingerprint function.

    Args:
        X_df (pd.DataFrame): Input DataFrame containing at least a "smiles" column.
        fingerprint_fn (function): Function to calculate fingerprints from SMILES.
        fingerprint_name (str): Name to describe the type of fingerprint.

    Returns:
        pd.DataFrame: DataFrame where each row corresponds to the fingerprints of a compound.
    """
    if "smiles" not in X_df.columns:
        raise ValueError("Input DataFrame must contain a 'smiles' column.")
    
    fingerprints = []
    for smiles in X_df["smiles"]:
        fingerprints.append(fingerprint_fn(smiles))

    fingerprint_df = pd.DataFrame(fingerprints)
    fingerprint_df.columns = [f"{fingerprint_name}_{i}" for i in range(fingerprint_df.shape[1])]
    fingerprint_df["smiles"] = X_df["smiles"].values
    return fingerprint_df