from caddkit.api.chembl import get_chembl_id_by_uniprot, query_bioactivity, query_compounds
from caddkit.utils import convert_ic50_to_pic50
import pandas as pd

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

    def get_chembl_id(self):
        """
        Retrieves the ChEMBL ID for the given UniProt ID.

        Returns:
            str: The ChEMBL ID.
        """
        try:
            print(f"Fetching ChEMBL ID for UniProt ID: {self.uniprot_id}")
            chembl_id = get_chembl_id_by_uniprot(self.uniprot_id)
            print(f"ChEMBL ID found: {chembl_id}")
            return chembl_id
        except Exception as e:
            raise RuntimeError(f"Error fetching ChEMBL ID: {e}")

    def query_bioactivity_data(self, chembl_id):
        """
        Fetches bioactivity data from ChEMBL for the given ChEMBL ID.

        Parameters:
            chembl_id (str): The ChEMBL ID for which to query bioactivity data.

        Returns:
            pd.DataFrame: DataFrame containing bioactivity data.
        """
        try:
            print("Requesting bioactivity data...")
            bioactivities_df = query_bioactivity(chembl_id)
            print(f"Retrieved bioactivity data with {bioactivities_df.shape[0]} rows.")
            return bioactivities_df
        except Exception as e:
            raise RuntimeError(f"Error querying bioactivity data: {e}")

    def process_bioactivity_data(self, bioactivities_df):
        """
        Processes the bioactivity data to clean and format it.

        Parameters:
            bioactivities_df (pd.DataFrame): Raw bioactivity data.

        Returns:
            pd.DataFrame: Processed bioactivity data.
        """
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
            return bioactivities_df
        except Exception as e:
            raise RuntimeError(f"Error processing bioactivity data: {e}")

    def query_compound_data(self, molecule_chembl_ids):
        """
        Fetches compound data from ChEMBL for the given list of molecule ChEMBL IDs.

        Parameters:
            molecule_chembl_ids (list): List of molecule ChEMBL IDs to query.

        Returns:
            pd.DataFrame: DataFrame containing compound data.
        """
        try:
            print("Requesting compound data for bioactivity hits...")
            compounds_df = query_compounds(molecule_chembl_ids)
            print(f"Retrieved compound data with {compounds_df.shape[0]} rows.")
            return compounds_df
        except Exception as e:
            raise RuntimeError(f"Error querying compound data: {e}")

    def process_compound_data(self, compounds_df):
        """
        Processes the compound data to extract canonical SMILES and clean it.

        Parameters:
            compounds_df (pd.DataFrame): Raw compound data.

        Returns:
            pd.DataFrame: Processed compound data with canonical SMILES.
        """
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
            return compounds_df
        except Exception as e:
            raise RuntimeError(f"Error processing compound data: {e}")

    def merge_data(self, bioactivities_df, compounds_df):
        """
        Merges the processed bioactivity and compound data into a single DataFrame.

        Parameters:
            bioactivities_df (pd.DataFrame): Processed bioactivity data.
            compounds_df (pd.DataFrame): Processed compound data.

        Returns:
            pd.DataFrame: Merged DataFrame containing bioactivity and compound data.
        """
        try:
            print("Merging bioactivity and compound data...")
            output_df = pd.merge(
                bioactivities_df[["molecule_chembl_id", "IC50", "units"]],
                compounds_df,
                on="molecule_chembl_id",
            )
            output_df.reset_index(drop=True, inplace=True)
            print(f"Merged data contains {output_df.shape[0]} entries.")
            return output_df
        except Exception as e:
            raise RuntimeError(f"Error merging data: {e}")

    def convert_ic50_to_pic50(self, output_df):
        """
        Converts IC50 values to pIC50 and sorts the data.

        Parameters:
            output_df (pd.DataFrame): DataFrame containing IC50 values.

        Returns:
            pd.DataFrame: DataFrame with pIC50 values and sorted by pIC50.
        """
        try:
            print("Converting IC50 to pIC50...")
            output_df["pIC50"] = output_df["IC50"].apply(convert_ic50_to_pic50)
            output_df.dropna(subset=["pIC50"], inplace=True)
            output_df.sort_values(by="pIC50", ascending=False, inplace=True)
            output_df.reset_index(drop=True, inplace=True)
            output_df.drop(["units", "IC50"], axis=1, inplace=True)
            print(f"Final dataset ready with {output_df.shape[0]} entries.")
            return output_df
        except Exception as e:
            raise RuntimeError(f"Error converting IC50 to pIC50: {e}")

    def run(self):
        """
        Executes the entire pipeline by calling individual steps:
        - Retrieves ChEMBL ID for the given UniProt ID.
        - Fetches and processes bioactivity and compound data.
        - Merges and converts data into the final DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the final processed data with SMILES and pIC50 values.
        """
        try:
            print("Starting the data processing pipeline...")

            # Step 1: Get ChEMBL ID
            chembl_id = self.get_chembl_id()

            # Step 2: Query bioactivity data
            bioactivities_df = self.query_bioactivity_data(chembl_id)

            # Step 3: Process bioactivity data
            bioactivities_df = self.process_bioactivity_data(bioactivities_df)

            # Step 4: Query compound data
            compounds_df = self.query_compound_data(bioactivities_df["molecule_chembl_id"].tolist())

            # Step 5: Process compound data
            compounds_df = self.process_compound_data(compounds_df)

            # Step 6: Merge data
            merged_df = self.merge_data(bioactivities_df, compounds_df)

            # Step 7: Convert IC50 to pIC50
            final_df = self.convert_ic50_to_pic50(merged_df)

            return final_df

        except Exception as e:
            print(f"Pipeline failed: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of erro