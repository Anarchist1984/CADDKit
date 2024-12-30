import pandas as pd
from chembl_webresource_client.new_client import new_client

def get_target_by_uniprot(uniprot_id):
    """
    Retrieves target information from ChEMBL for a given UniProt ID.

    This function queries the ChEMBL database to fetch target details for the 
    specified UniProt ID. It returns the results as a pandas DataFrame containing 
    fields such as 'target_chembl_id', 'organism', 'pref_name', and 'target_type'.

    Parameters:
        uniprot_id (str): The UniProt ID for which target information is to be fetched.

    Returns:
        pd.DataFrame: A DataFrame containing target information. If no results are found 
        or an error occurs, an empty DataFrame is returned.

    Raises:
        ValueError: If no targets are found for the provided UniProt ID.
        TypeError: If the provided UniProt ID is not a string.
    """
    try:
        # Validate input type
        if not isinstance(uniprot_id, str):
            raise TypeError("The UniProt ID must be a string.")

        # Initialize ChEMBL target API client
        targets_api = new_client.target
        
        # Query the API
        targets = targets_api.filter(target_components__accession=uniprot_id).only(
            "target_chembl_id", "organism", "pref_name", "target_type"
        )
        targets_df = pd.DataFrame.from_records(targets)
        
        # Check if any targets were found
        if targets_df.empty:
            raise ValueError(f"No targets found for UniProt ID: {uniprot_id}")
        
        return targets_df
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return pd.DataFrame()  # Return an empty DataFrame
    
    except TypeError as te:
        print(f"TypeError: {te}")
        return pd.DataFrame()  # Return an empty DataFrame
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame
    
def get_chembl_id(uniprot_id, loc=0):
    """
    Retrieves the ChEMBL ID for a target corresponding to a given UniProt ID.

    This function uses the `get_target_by_uniprot` function to fetch targets for the 
    specified UniProt ID and returns the ChEMBL ID of the target at the specified 
    location in the results.

    Parameters:
        uniprot_id (str): The UniProt ID for which the ChEMBL ID is to be retrieved.
        loc (int, optional): The index of the target in the results list to retrieve. Defaults to 0.

    Returns:
        str: The ChEMBL ID of the selected target.

    Raises:
        IndexError: If the specified index `loc` is out of bounds for the target results.
        KeyError: If the 'target_chembl_id' column is not present in the results DataFrame.
        Exception: For any unexpected errors during execution.
    """
    try:
        # Fetch targets for the given UniProt ID
        targets = get_target_by_uniprot(uniprot_id)
        
        # Retrieve the target at the specified location
        target = targets.iloc[loc]
        
        # Return the ChEMBL ID
        return target['target_chembl_id']
    
    except IndexError:
        print(f"IndexError: The specified index {loc} is out of bounds.")
        return None  # Return None if the index is invalid

    except KeyError:
        print("KeyError: 'target_chembl_id' column not found in the results.")
        return None  # Return None if the column is missing

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None  # Return None for any other errors

if __name__ == "__main__":
    get_chembl_id('P00533')