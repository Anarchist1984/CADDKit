import biotite.database.rcsb as rcsb
import pypdb
import redo
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def query_by_uniprot_id(uniprot_id: str) -> rcsb.FieldQuery:
    """
    Create a query to search by UniProt ID.

    Args:
        uniprot_id (str): The UniProt ID to search for. Must be a non-empty string.

    Returns:
        rcsb.FieldQuery: The query object for the UniProt ID.

    Raises:
        ValueError: If `uniprot_id` is not a valid string.
    """
    if not isinstance(uniprot_id, str) or not uniprot_id.strip():
        raise ValueError("`uniprot_id` must be a non-empty string.")
    return rcsb.FieldQuery(
        "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
        exact_match=uniprot_id,
    )


def query_by_deposition_date(before_deposition_date: str) -> rcsb.FieldQuery:
    """
    Create a query to search by deposition date.

    Args:
        before_deposition_date (str): The latest deposition date to search for in 'YYYY-MM-DD' format.

    Returns:
        rcsb.FieldQuery: The query object for the deposition date.

    Raises:
        ValueError: If `before_deposition_date` is not a valid date string.
    """
    if not isinstance(before_deposition_date, str) or not before_deposition_date.strip():
        raise ValueError("`before_deposition_date` must be a non-empty string in 'YYYY-MM-DD' format.")
    return rcsb.FieldQuery(
        "rcsb_accession_info.deposit_date", less=before_deposition_date
    )


def query_by_experimental_method(experimental_method: str) -> rcsb.FieldQuery:
    """
    Create a query to search by experimental method.

    Args:
        experimental_method (str): The experimental method to search for.

    Returns:
        rcsb.FieldQuery: The query object for the experimental method.

    Raises:
        ValueError: If `experimental_method` is not a valid string.
    """
    if not isinstance(experimental_method, str) or not experimental_method.strip():
        raise ValueError("`experimental_method` must be a non-empty string.")
    return rcsb.FieldQuery("exptl.method", exact_match=experimental_method)


def query_by_resolution(max_resolution: float) -> rcsb.FieldQuery:
    """
    Create a query to search by resolution.

    Args:
        max_resolution (float): The maximum resolution to search for.

    Returns:
        rcsb.FieldQuery: The query object for the resolution.

    Raises:
        ValueError: If `max_resolution` is not a positive float.
    """
    if not isinstance(max_resolution, (float, int)) or max_resolution <= 0:
        raise ValueError("`max_resolution` must be a positive number.")
    return rcsb.FieldQuery(
        "rcsb_entry_info.resolution_combined", less_or_equal=max_resolution
    )


def query_by_polymer_count(n_chains: int) -> rcsb.FieldQuery:
    """
    Create a query to search by polymer count.

    Args:
        n_chains (int): The number of polymer chains to search for.

    Returns:
        rcsb.FieldQuery: The query object for the polymer count.

    Raises:
        ValueError: If `n_chains` is not a non-negative integer.
    """
    if not isinstance(n_chains, int) or n_chains < 0:
        raise ValueError("`n_chains` must be a non-negative integer.")
    return rcsb.FieldQuery(
        "rcsb_entry_info.deposited_polymer_entity_instance_count", equals=n_chains
    )


def query_by_ligand_mw(min_ligand_molecular_weight: float) -> rcsb.FieldQuery:
    """
    Create a query to search by ligand molecular weight.

    Args:
        min_ligand_molecular_weight (float): The minimum ligand molecular weight to search for.

    Returns:
        rcsb.FieldQuery: The query object for the ligand molecular weight.

    Raises:
        ValueError: If `min_ligand_molecular_weight` is not a positive float.
    """
    if not isinstance(min_ligand_molecular_weight, (float, int)) or min_ligand_molecular_weight <= 0:
        raise ValueError("`min_ligand_molecular_weight` must be a positive number.")
    return rcsb.FieldQuery(
        "chem_comp.formula_weight", molecular_definition=True, greater=min_ligand_molecular_weight
    )


def search_pdb(
    uniprot_id: str = None,
    before_deposition_date: str = None,
    experimental_method: str = None,
    max_resolution: float = None,
    n_chains: int = None,
    min_ligand_molecular_weight: float = None,
) -> list:
    """
    Search the RCSB PDB database using a combination of query fields.

    Args:
        uniprot_id (str, optional): UniProt ID to search for.
        before_deposition_date (str, optional): Latest deposition date ('YYYY-MM-DD').
        experimental_method (str, optional): Experimental method to search for.
        max_resolution (float, optional): Maximum resolution to search for.
        n_chains (int, optional): Number of polymer chains to search for.
        min_ligand_molecular_weight (float, optional): Minimum ligand molecular weight.

    Returns:
        list: List of matching PDB IDs.

    Raises:
        ValueError: If no search criteria are provided.
    """
    queries = []
    if uniprot_id:
        queries.append(query_by_uniprot_id(uniprot_id))
    if before_deposition_date:
        queries.append(query_by_deposition_date(before_deposition_date))
    if experimental_method:
        queries.append(query_by_experimental_method(experimental_method))
    if max_resolution:
        queries.append(query_by_resolution(max_resolution))
    if n_chains:
        queries.append(query_by_polymer_count(n_chains))
    if min_ligand_molecular_weight:
        queries.append(query_by_ligand_mw(min_ligand_molecular_weight))

    if not queries:
        raise ValueError("At least one search criteria must be provided.")

    composite_query = rcsb.CompositeQuery(queries, "and")
    pdb_ids = rcsb.search(composite_query)

    return pdb_ids


@redo.retriable(attempts=10, sleeptime=2)
def describe_one_pdb_id(pdb_id: str) -> dict:
    """
    Fetch meta information from the PDB database.

    Args:
        pdb_id (str): The PDB ID to fetch metadata for.

    Returns:
        dict: Metadata information for the specified PDB ID.

    Raises:
        ValueError: If fetching metadata fails after retries.
    """
    described = pypdb.describe_pdb(pdb_id)
    if described is None:
        raise ValueError(f"Could not fetch metadata for PDB ID: {pdb_id}")
    return described


def fetch_pdb_metadata(pdb_ids: list) -> list:
    """
    Fetch metadata for a list of PDB IDs with retry functionality.

    Args:
        pdb_ids (list): List of PDB IDs to fetch metadata for.

    Returns:
        list: List of metadata dictionaries for each PDB ID.
    """
    return [describe_one_pdb_id(pdb_id) for pdb_id in tqdm(pdb_ids)]


def get_ligands(pdb_id: str) -> dict:
    """
    Fetch ligand information for a given PDB ID.

    Args:
        pdb_id (str): The PDB ID to fetch ligand information for.

    Returns:
        dict: Ligand information.

    Raises:
        requests.RequestException: If fetching ligand information fails.
    """
    pdb_info = _fetch_pdb_nonpolymer_info(pdb_id)
    ligand_expo_ids = [
        entity["pdbx_entity_nonpoly"]["comp_id"]
        for entity in pdb_info["data"]["entry"]["nonpolymer_entities"]
    ]
    return {ligand: _fetch_ligand_expo_info(ligand) for ligand in ligand_expo_ids}


def _fetch_pdb_nonpolymer_info(pdb_id: str) -> dict:
    query = f"""
    {{
        entry(entry_id: "{pdb_id}") {{
            nonpolymer_entities {{
                pdbx_entity_nonpoly {{
                    comp_id
                }}
            }}
        }}
    }}
    """
    url = f"https://data.rcsb.org/graphql?query={query}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def _fetch_ligand_expo_info(ligand_expo_id: str) -> dict:
    url = f"http://ligand-expo.rcsb.org/reports/{ligand_expo_id[0]}/{ligand_expo_id}/"
    response = requests.get(url)
    response.raise_for_status()
    html = BeautifulSoup(response.text, "html.parser")
    info = {
        row.find_all("td")[0].text.strip(): row.find_all("td")[1].text.strip()
        for table in html.find_all("table")
        for row in table.find_all("tr")
        if len(row.find_all("td")) == 2
    }
    return info

if __name__ == "__main__":
    def test_query_by_deposition_date():
        query = query_by_deposition_date("2021-01-01")
        print(query.__dict__)  # This will display all attributes of the `query` object
    def test_query_by_experimental_method():
        query = query_by_experimental_method("X-ray diffraction")
        print(query.__dict__)
    def test_query_by_resolution():
        query = query_by_resolution(2.0)
        print(query.__dict__)
    def test_query_by_polymer_count():
        query = query_by_polymer_count(2)
        print(query.__dict__)
    def test_query_by_ligand_mw():
        query = query_by_ligand_mw(100)
        print(query.__dict__)
    test_query_by_deposition_date()
    test_query_by_experimental_method()
    test_query_by_resolution()
    test_query_by_polymer_count()
    test_query_by_ligand_mw()