import pandas as pd
from chembl_webresource_client.new_client import new_client
from tqdm.auto import tqdm


def get_chembl_targets_by_uniprot(uniprot_id):
    """
    Retrieves target information from ChEMBL for a given UniProt ID.

    This function queries the ChEMBL database to fetch target details for the
    specified UniProt ID. It returns the results as a pandas DataFrame
    containing fields such as 'target_chembl_id', 'organism', 'pref_name',
    and 'target_type'.

    Parameters:
        uniprot_id (str): The UniProt ID for which target information is to be
            fetched.

    Returns:
        pd.DataFrame: A DataFrame containing target information. If no results
        are found or an error occurs, an empty DataFrame is returned.

    Raises:
        ValueError: If no targets are found for the provided UniProt ID.
        TypeError: If the provided UniProt ID is not a string.
    """
    try:
        if not isinstance(uniprot_id, str):
            raise TypeError("The UniProt ID must be a string.")

        targets_api = new_client.target
        targets = targets_api.filter(
            target_components__accession=uniprot_id
        ).only("target_chembl_id", "organism", "pref_name", "target_type")
        targets_df = pd.DataFrame.from_records(targets)

        if targets_df.empty:
            raise ValueError(f"No targets found for UniProt ID: {uniprot_id}")
        return targets_df

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return pd.DataFrame()

    except TypeError as te:
        print(f"TypeError: {te}")
        return pd.DataFrame()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()


def get_chembl_id_by_uniprot(uniprot_id, loc=0):
    """
    Retrieves the ChEMBL ID for a target corresponding to a given UniProt ID.

    Parameters:
        uniprot_id (str): The UniProt ID for which the ChEMBL ID is to be
            retrieved.
        loc (int, optional): The index of the target in the results list to
            retrieve. Defaults to 0.

    Returns:
        str: The ChEMBL ID of the selected target.

    Raises:
        IndexError: If the specified index `loc` is out of bounds for the
            target results.
        KeyError: If the 'target_chembl_id' column is not present in the
            results DataFrame.
    """
    try:
        targets = get_chembl_targets_by_uniprot(uniprot_id)
        target = targets.iloc[loc]
        return target["target_chembl_id"]

    except IndexError:
        print(f"IndexError: The specified index {loc} is out of bounds.")
        return None

    except KeyError:
        print("KeyError: 'target_chembl_id' column not found in the results.")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def query_chembl_bioactivity(chembl_id):
    """
    Queries bioactivity data from ChEMBL for a given target ChEMBL ID.

    Parameters:
        chembl_id (str): The ChEMBL ID of the target for which bioactivity
            data is to be queried.

    Returns:
        pd.DataFrame: A DataFrame containing bioactivity data. If no data is
        found or an error occurs, an empty DataFrame is returned.
    """
    try:
        bioactivities_api = new_client.activity
        bioactivities = bioactivities_api.filter(
            target_chembl_id=chembl_id,
            type="IC50",
            relation="=",
            assay_type="B",
        ).only(
            "activity_id",
            "assay_chembl_id",
            "assay_description",
            "assay_type",
            "molecule_chembl_id",
            "type",
            "standard_units",
            "relation",
            "standard_value",
            "target_chembl_id",
            "target_organism",
        )
        bioactivities_df = pd.DataFrame.from_dict(bioactivities)

        if bioactivities_df.empty:
            print(f"No bioactivity data found for ChEMBL ID: {chembl_id}")

        return bioactivities_df

    except Exception as e:
        print(f"An error occurred while querying bioactivity data: {e}")
        return pd.DataFrame()


def query_chembl_compounds(compounds_list):
    """
    Queries compound data from ChEMBL for a given list of molecule ChEMBL IDs.

    Parameters:
        compounds_list (list): A list of molecule ChEMBL IDs to query.

    Returns:
        pd.DataFrame: A DataFrame containing the ChEMBL IDs and molecular
        structures of the compounds. If an error occurs, an empty DataFrame
        is returned.
    """
    try:
        compounds_api = new_client.molecule
        compounds_provider = compounds_api.filter(
            molecule_chembl_id__in=list(compounds_list)
        ).only("molecule_chembl_id", "molecule_structures")

        compounds = list(tqdm(compounds_provider, desc="Fetching compounds"))
        compounds_df = pd.DataFrame.from_records(compounds)

        return compounds_df

    except Exception as e:
        print(f"An error occurred while querying compounds: {e}")
        return pd.DataFrame()