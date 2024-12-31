import pandas as pd
from molpharm.filters import calculate_ro5_properties, calculate_soft_reos_properties

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
        Initializes the MolecularFilter with empty filter and filter name lists.
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

    def process(self, smiles_list, include_columns=None):
        """
        Processes a list of SMILES strings through all added filters.

        Parameters
        ----------
        smiles_list : list of str
            List of SMILES strings representing molecules.
        include_columns : list of str, optional
            Specific columns from filter measurements to include in the output DataFrames.

        Returns
        -------
        filtered_df : pandas.DataFrame
            DataFrame of molecules that passed all filters.
        violated_df : pandas.DataFrame
            DataFrame of molecules that violated at least one filter, with reasons for violation.

        Raises
        ------
        ValueError
            If smiles_list is not a list or contains non-string elements.
        KeyError
            If any of the include_columns do not exist in the filter results.
        """
        if not isinstance(smiles_list, list) or not all(isinstance(smiles, str) for smiles in smiles_list):
            raise ValueError("smiles_list must be a list of strings.")

        results = []
        violation_reasons = []

        for smiles in smiles_list:
            molecule_data = {"smiles": smiles}
            violated = False
            reasons = []

            for filter_func, name in zip(self.filters, self.filter_names):
                try:
                    filter_result = filter_func(smiles)
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

        df = pd.DataFrame(results)
        df["violation_reason"] = violation_reasons

        # Separate passed and violated molecules
        filtered_df = df[df["violated"] == False].copy()
        violated_df = df[df["violated"] == True].copy()

        # Include only specified columns if provided
        if include_columns:
            try:
                filtered_df = filtered_df[["smiles"] + include_columns]
                violated_df = violated_df[["smiles", "violation_reason"] + include_columns]
            except KeyError as e:
                raise KeyError(f"One or more columns specified in include_columns are missing: {e}")
        else:
            # Default to including only minimal columns if none are specified
            filtered_df = filtered_df[["smiles"]]
            violated_df = violated_df[["smiles", "violation_reason"]]

        return filtered_df, violated_df

if __name__=="__main__":
    smiles_list = [
        "CCO",  # Ethanol
        "CCN(CC)CC",  # Triethylamine
        "C1=CC=C(C=C1)C(=O)O"  # Benzoic acid
    ]

    for smiles in smiles_list:
        ro5_properties = calculate_ro5_properties(smiles)
        soft_reos_properties = calculate_soft_reos_properties(smiles)

        print(ro5_properties)
        print(soft_reos_properties)
    filter = CompoundFilter()

    filter.add_filter(calculate_ro5_properties, "ro5_properties")
    filter.add_filter(calculate_soft_reos_properties, "soft_reos_properties")

    filtered, violated = filter.process(smiles_list)
    filtered
    violated