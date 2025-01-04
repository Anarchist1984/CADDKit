from rdkit import Chem, AllChem, DataStructs
import numpy as np

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
        