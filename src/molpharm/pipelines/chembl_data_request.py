from molpharm.chembl import get_chembl_id, query_bioactivity, query_compounds
from molpharm.utils import convert_ic50_to_pic50
import pandas as pd

import pandas as pd
import numpy as np


class DataRequestPipeline:
    """
    A pipeline to fetch, process, and merge bioactivity and compound data 
    from ChEMBL for a given UniProt ID.
    """

    def __init__(self, uniprot_id):
        """
        Initializes the DataRequestPipeline with the UniProt ID.

        Parameters:
            uniprot_id (str): The UniProt ID for the target protein.
        """
        self.uniprot_id = uniprot_id
        print(f"Pipeline initialized with UniProt ID: {self.uniprot_id}")

    def process(self):
        """
        Executes the data pipeline:
        - Retrieves ChEMBL ID for the given UniProt ID.
        - Fetches bioactivity data for the ChEMBL ID.
        - Fetches compound data for the bioactivity hits.
        - Processes, filters, and merges the data into a final DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the processed data with SMILES and pIC50 values.
        """
        try:
            print("Starting the data processing pipeline...")

            # Step 1: Get ChEMBL ID
            try:
                print(f"Fetching ChEMBL ID for UniProt ID: {self.uniprot_id}")
                chembl_id = get_chembl_id(self.uniprot_id)
                print(f"ChEMBL ID found: {chembl_id}")
            except Exception as e:
                raise RuntimeError(f"Error fetching ChEMBL ID: {e}")

            # Step 2: Query bioactivity data
            try:
                print("Requesting bioactivity data...")
                bioactivities_df = query_bioactivity(chembl_id)
                print(f"Retrieved bioactivity data with {bioactivities_df.shape[0]} rows.")
            except Exception as e:
                raise RuntimeError(f"Error querying bioactivity data: {e}")

            # Step 3: Process bioactivity data
            try:
                print("Processing bioactivity data...")
                bioactivities_df.drop(["units", "value"], axis=1, inplace=True)
                bioactivities_df = bioactivities_df.astype({"standard_value": "float64"})
                bioactivities_df.dropna(axis=0, inplace=True)
                bioactivities_df = bioactivities_df[bioactivities_df["standard_units"] == "nM"]
                bioactivities_df.drop_duplicates("molecule_chembl_id", inplace=True)
                bioactivities_df.reset_index(drop=True, inplace=True)
                bioactivities_df.rename(columns={"standard_value": "IC50", "standard_units": "units"}, inplace=True)
                print(f"Bioactivity data processed. Remaining {bioactivities_df.shape[0]} entries.")
            except Exception as e:
                raise RuntimeError(f"Error processing bioactivity data: {e}")

            # Step 4: Query compound data
            try:
                print("Requesting compound data for bioactivity hits...")
                compounds_df = query_compounds(bioactivities_df["molecule_chembl_id"].tolist())
                print(f"Retrieved compound data with {compounds_df.shape[0]} rows.")
            except Exception as e:
                raise RuntimeError(f"Error querying compound data: {e}")

            # Step 5: Process compound data
            try:
                print("Processing compound data...")
                compounds_df.dropna(axis=0, inplace=True)
                compounds_df.drop_duplicates("molecule_chembl_id", inplace=True)
                compounds_df.reset_index(drop=True, inplace=True)
                canonical_smiles = []
                for i, compounds in compounds_df.iterrows():
                    try:
                        canonical_smiles.append(compounds["molecule_structures"]["canonical_smiles"])
                    except KeyError:
                        canonical_smiles.append(None)
                compounds_df["smiles"] = canonical_smiles
                compounds_df.drop("molecule_structures", axis=1, inplace=True)
                print(f"Canonical SMILES extracted for {len(canonical_smiles)} compounds.")
            except Exception as e:
                raise RuntimeError(f"Error processing compound data: {e}")

            # Step 6: Merge data
            try:
                print("Merging bioactivity and compound data...")
                output_df = pd.merge(
                    bioactivities_df[["molecule_chembl_id", "IC50", "units"]],
                    compounds_df,
                    on="molecule_chembl_id",
                )
                output_df.reset_index(drop=True, inplace=True)
                print(f"Merged data contains {output_df.shape[0]} entries.")
            except Exception as e:
                raise RuntimeError(f"Error merging data: {e}")

            # Step 7: Convert IC50 to pIC50
            try:
                print("Converting IC50 to pIC50...")
                output_df["pIC50"] = output_df["IC50"].apply(convert_ic50_to_pic50)
                output_df.dropna(subset=["pIC50"], inplace=True)
                output_df.sort_values(by="pIC50", ascending=False, inplace=True)
                output_df.reset_index(drop=True, inplace=True)
                output_df.drop(["units", "IC50"], axis=1, inplace=True)
                print(f"Final dataset ready with {output_df.shape[0]} entries.")
            except Exception as e:
                raise RuntimeError(f"Error converting IC50 to pIC50: {e}")

            return output_df

        except Exception as e:
            print(f"Pipeline failed: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error