from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, MACCSkeys, rdFingerprintGenerator
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
    
def calculate_maccs_fingerprint_as_bit_vect(smiles):
    """
    Calculate MACCS fingerprints for a given SMILES string.
    Args:
        smiles (str): SMILES string for the compound.

    Returns:
        np.array: The computed MACCS fingerprint or zeros if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        return np.array(MACCSkeys.GenMACCSKeys(mol))
    else:
        return np.zeros(167, dtype=np.float32)
    
def calculate_morgan2_fingerprint_as_bit_vect(smiles,  n_bits=2048):
    """
    Calculate Morgan fingerprints for a given SMILES string.
    Args:
        smiles (str): SMILES string for the compound.

    Returns:
        np.array: The computed Morgan fingerprint or zeros if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fpg = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=n_bits)
        return np.array(fpg.GetCountFingerprint(mol))
    else:
        return np.zeros(2048, dtype=np.float32)
    
def calculate_morgan3_fingerprint_as_bit_vect(smiles, n_bits=2048):
    """
    Calculate Morgan fingerprints for a given SMILES string.
    Args:
        smiles (str): SMILES string for the compound.

    Returns:
        np.array: The computed Morgan fingerprint or zeros if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        fpg = rdFingerprintGenerator.GetMorganGenerator(radius=3, fpSize=n_bits)
        return np.array(fpg.GetCountFingerprint(mol))
    else:
        return np.zeros(2048, dtype=np.float32)
        
def generate_fingerprint_dfs(X_df, fingerprint_fn, smiles_col="smiles", fp_column_name=""):
    """
    Generate a DataFrame with fingerprints for a given input DataFrame and fingerprint function,
    while retaining the original columns.

    Args:
        X_df (pd.DataFrame): Input DataFrame containing at least a column specified by `smiles_col`.
        fingerprint_fn (function): Function to calculate fingerprints from SMILES.
        smiles_col (str): Column name containing SMILES strings. Default is "smiles".

    Returns:
        pd.DataFrame: DataFrame where each row corresponds to the original columns and the fingerprints of a compound.

    Raises:
        ValueError: If the specified `smiles_col` is not in the input DataFrame.
    """
    if smiles_col not in X_df.columns:
        raise ValueError(f"Input DataFrame must contain a '{smiles_col}' column.")
    
    total_rows = len(X_df)
    fingerprints = []
    for i, smiles in enumerate(X_df[smiles_col]):
        fingerprints.append(fingerprint_fn(smiles))
        print(f"Generated fingerprints for {i + 1} out of {total_rows} rows.")
    
    fingerprint_df = pd.DataFrame(fingerprints)
    fingerprint_df.columns = [f"{fp_column_name}{i}" for i in range(fingerprint_df.shape[1])]
    
    # Concatenate the original DataFrame with the fingerprint DataFrame
    result_df = pd.concat([X_df.reset_index(drop=True), fingerprint_df], axis=1)
    return result_df

def generate_fingerprint_dfs_to_csv(
    X_df,
    fingerprint_fn,
    output_csv_path,
    smiles_col="smiles",
    fp_column_name="",
    chunk_size=100
):
    """
    Generate fingerprints for a DataFrame and write them incrementally into a CSV file,
    with error handling and progress tracking.

    Args:
        X_df (pd.DataFrame): Input DataFrame containing at least a column specified by `smiles_col`.
        fingerprint_fn (function): Function to calculate fingerprints from SMILES.
        output_csv_path (str): Path to the output CSV file.
        smiles_col (str): Column name containing SMILES strings. Default is "smiles".
        fp_column_name (str): Prefix for fingerprint column names. Default is "".
        chunk_size (int): Number of rows to process in each batch before writing to CSV. Default is 100.

    Returns:
        None

    Raises:
        ValueError: If the specified `smiles_col` is not in the input DataFrame.
    """
    if smiles_col not in X_df.columns:
        raise ValueError(f"Input DataFrame must contain a '{smiles_col}' column.")
    
    # Prepare the output CSV file
    if os.path.exists(output_csv_path):
        os.remove(output_csv_path)  # Remove existing file to avoid appending issues

    total_rows = len(X_df)

    # Set up the progress bar
    with tqdm(total=total_rows, desc="Generating fingerprints", unit="rows") as pbar:
        for start_idx in range(0, total_rows, chunk_size):
            chunk = X_df.iloc[start_idx:start_idx + chunk_size]
            fingerprints = []

            for smiles in chunk[smiles_col]:
                try:
                    # Generate fingerprints
                    fingerprints.append(fingerprint_fn(smiles))
                except Exception as e:
                    # Log the error and continue
                    fingerprints.append([None])  # Append placeholder for failed fingerprint
                    pass  # Skip the error silently

            # Create a DataFrame for fingerprints
            fingerprint_df = pd.DataFrame(fingerprints)
            fingerprint_df.columns = [f"{fp_column_name}{i}" for i in range(fingerprint_df.shape[1])]

            # Concatenate the original chunk with the fingerprint DataFrame
            result_chunk = pd.concat([chunk.reset_index(drop=True), fingerprint_df], axis=1)

            # Append the result to the CSV file
            result_chunk.to_csv(output_csv_path, mode='a', index=False, header=not os.path.exists(output_csv_path))

            # Update the progress bar
            pbar.update(len(chunk))