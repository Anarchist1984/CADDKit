"""
This module provides tools to evaluate chemical properties of molecules and apply
various filtering criteria for drug discovery, based on chemical rules such as 
Lipinski's Rule of Five and REOS (Rule of Five-like criteria). It includes utility 
functions for individual molecule evaluation and a `CompoundFilter` class for 
batch processing and filtering.

Main Functionalities
--------------------
1. Calculate Lipinski's Rule of Five properties for a molecule.
2. Evaluate a molecule against softened REOS criteria.
3. Apply multiple filtering rules to a dataset of molecules.

Dependencies
------------
- pandas
- RDKit

Functions
---------
- calculate_ro5_properties(smiles):
    Tests if a molecule complies with Lipinski's Rule of Five.
- calculate_soft_reos_properties(smiles):
    Tests if a molecule meets the softened REOS criteria.

Classes
-------
- CompoundFilter:
    A class for applying multiple filters to a dataset of molecules and 
    tracking compliance or violations.

Examples
--------
1. Evaluate a single molecule against Lipinski's Rule of Five:
    >>> calculate_ro5_properties("CCO")
    molecular_weight    46.041864
    n_hba                1.000000
    n_hbd                1.000000
    logp                -0.001387
    fulfilled            True
    dtype: float64

2. Evaluate a batch of molecules using CompoundFilter:
    >>> filter = CompoundFilter()
    >>> filter.add_filter(calculate_ro5_properties, "Lipinski's Rule of Five")
    >>> smiles_list = ["CCO", "CCCCC"]
    >>> filtered, violated = filter.process(smiles_list)
    >>> print(filtered)
       smiles
    0     CCO
"""

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
        index=["molecular_weight",
               "heavy_atoms", 
               "rotatable_bonds", 
               "n_hba", 
               "n_hbd", 
               "logp", 
               "fulfilled"]
    )

class CompoundFilter:
    """
    A class to apply multiple filters to a dataset of molecules represented by SMILES strings.

    Attributes
    ----------
    filters : list of callable
        A list of filter functions to apply to the molecules.
    filter_names : list of str
        Names of the filters for tracking violations.
    """
    
    def __init__(self):
        """
        Initializes the CompoundFilter with empty filter and filter name lists.
        """
        self.filters = []
        self.filter_names = []

    def add_filter(self, filter_func, name):
        """
        Adds a filter function to the filter list.

        Parameters
        ----------
        filter_func : callable
            A function that takes a SMILES string as input and returns a pandas.Series 
            with measurements and a 'fulfilled' boolean indicating compliance.
        name : str
            Name of the filter for tracking violations.

        Raises
        ------
        ValueError
            If the provided filter_func is not callable.
        TypeError
            If the name is not a string.
        """
        if not callable(filter_func):
            raise ValueError("The provided filter_func must be callable.")
        if not isinstance(name, str):
            raise TypeError("The filter name must be a string.")

        self.filters.append(filter_func)
        self.filter_names.append(name)

    def process(self, df, smiles_column):
        """
        Processes a DataFrame of molecules through all added filters.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame containing molecule data, including a column with SMILES strings.
        smiles_column : str
            The column name containing SMILES strings.

        Returns
        -------
        filtered_df : pandas.DataFrame
            DataFrame of molecules that passed all filters, retaining all original columns.
        violated_df : pandas.DataFrame
            DataFrame of molecules that violated at least one filter, retaining all original columns
            and adding a column for reasons of violation.

        Raises
        ------
        KeyError
            If the smiles_column does not exist in the DataFrame.
        """
        if smiles_column not in df.columns:
            raise KeyError(f"The specified SMILES column '{smiles_column}' is not in the DataFrame.")

        results = []
        violation_reasons = []

        for _, row in df.iterrows():
            molecule_data = row.to_dict()  # Retain all original columns
            smiles = row[smiles_column]
            violated = False
            reasons = []

            for filter_func, name in zip(self.filters, self.filter_names):
                try:
                    filter_result = filter_func(smiles)
                    # Only keep original columns in the final result
                    molecule_data.update(filter_result.to_dict())
                    if not filter_result["fulfilled"]:
                        violated = True
                        reasons.append(name)
                except Exception as e:
                    violated = True
                    reasons.append(f"{name}: {str(e)}")
                    break

            molecule_data["violated"] = violated
            violation_reasons.append(", ".join(reasons))
            results.append(molecule_data)

        # Create resulting DataFrame
        result_df = pd.DataFrame(results)
        result_df["violation_reason"] = violation_reasons

        # Separate passed and violated molecules
        filtered_df = result_df[result_df["violated"] == False].copy()
        violated_df = result_df[result_df["violated"] == True].copy()

        # Ensure only original columns are in the final DataFrames
        original_columns = df.columns.tolist()
        filtered_df = filtered_df[original_columns]
        violated_df = violated_df[original_columns + ['violation_reason']]

        return filtered_df, violated_df
