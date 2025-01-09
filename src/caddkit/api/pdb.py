from typing import List, Dict, Optional
import biotite.database.rcsb as rcsb
import pypdb
import redo
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def create_query_by_uniprot_id(uniprot_id: str) -> rcsb.FieldQuery:
    """
    Generate a query to search by UniProt ID.

    Args:
        uniprot_id (str): UniProt ID to search for.

    Returns:
        rcsb.FieldQuery: The query object for the UniProt ID.

    Raises:
        ValueError: If `uniprot_id` is not a valid non-empty string.
    """
    if not uniprot_id.strip():
        raise ValueError("`uniprot_id` must be a non-empty string.")
    return rcsb.FieldQuery(
        (
            "rcsb_polymer_entity_container_identifiers."
            "reference_sequence_identifiers.database_accession"
        ),
        exact_match=uniprot_id,
    )


def create_query_by_deposition_date(max_date: str) -> rcsb.FieldQuery:
    """
    Generate a query to search by deposition date.

    Args:
        max_date (str): Maximum deposition date in 'YYYY-MM-DD' format.

    Returns:
        rcsb.FieldQuery: The query object for the deposition date.

    Raises:
        ValueError: If `max_date` is not a valid non-empty string.
    """
    if not max_date.strip():
        raise ValueError(
            "`max_date` must be a non-empty string in 'YYYY-MM-DD' format."
        )
    return rcsb.FieldQuery("rcsb_accession_info.deposit_date", less=max_date)


def create_query_by_experimental_method(method: str) -> rcsb.FieldQuery:
    """
    Generate a query to search by experimental method.

    Args:
        method (str): Experimental method to search for.

    Returns:
        rcsb.FieldQuery: The query object for the experimental method.

    Raises:
        ValueError: If `method` is not a valid non-empty string.
    """
    if not method.strip():
        raise ValueError("`method` must be a non-empty string.")
    return rcsb.FieldQuery("exptl.method", exact_match=method)


def create_query_by_resolution(max_resolution: float) -> rcsb.FieldQuery:
    """
    Generate a query to search by resolution.

    Args:
        max_resolution (float): Maximum resolution.

    Returns:
        rcsb.FieldQuery: The query object for resolution.

    Raises:
        ValueError: If `max_resolution` is not a positive number.
    """
    if max_resolution <= 0:
        raise ValueError("`max_resolution` must be a positive number.")
    return rcsb.FieldQuery("rcsb_entry_info.resolution_combined",
                           less_or_equal=max_resolution)


def create_query_by_polymer_count(chain_count: int) -> rcsb.FieldQuery:
    """
    Generate a query to search by polymer chain count.

    Args:
        chain_count (int): Number of polymer chains.

    Returns:
        rcsb.FieldQuery: The query object for polymer chain count.

    Raises:
        ValueError: If `chain_count` is not a non-negative integer.
    """
    if chain_count < 0:
        raise ValueError("`chain_count` must be a non-negative integer.")
    return rcsb.FieldQuery(
        "rcsb_entry_info.deposited_polymer_entity_instance_count",
        equals=chain_count
    )


def create_query_by_ligand_weight(min_weight: float) -> rcsb.FieldQuery:
    """
    Generate a query to search by ligand molecular weight.

    Args:
        min_weight (float): Minimum ligand molecular weight.

    Returns:
        rcsb.FieldQuery: The query object for ligand molecular weight.

    Raises:
        ValueError: If `min_weight` is not a positive number.
    """
    if min_weight <= 0:
        raise ValueError("`min_weight` must be a positive number.")
    return rcsb.FieldQuery("chem_comp.formula_weight",
                           molecular_definition=True,
                           greater=min_weight)


def search_rcsb_pdb(
    uniprot_id: Optional[str] = None,
    max_deposition_date: Optional[str] = None,
    experimental_method: Optional[str] = None,
    max_resolution: Optional[float] = None,
    chain_count: Optional[int] = None,
    min_ligand_weight: Optional[float] = None,
) -> List[str]:
    """
    Search the RCSB PDB database using multiple criteria.

    Args:
        uniprot_id (str, optional): UniProt ID.
        max_deposition_date (str, optional): Maximum deposition date
        ('YYYY-MM-DD').
        experimental_method (str, optional): Experimental method.
        max_resolution (float, optional): Maximum resolution.
        chain_count (int, optional): Number of polymer chains.
        min_ligand_weight (float, optional): Minimum ligand molecular weight.

    Returns:
        List[str]: List of matching PDB IDs.

    Raises:
        ValueError: If no search criteria are provided.
    """
    queries = []
    if uniprot_id:
        queries.append(create_query_by_uniprot_id(uniprot_id))
    if max_deposition_date:
        queries.append(create_query_by_deposition_date(max_deposition_date))
    if experimental_method:
        queries.append(create_query_by_experimental_method(experimental_method))
    if max_resolution:
        queries.append(create_query_by_resolution(max_resolution))
    if chain_count:
        queries.append(create_query_by_polymer_count(chain_count))
    if min_ligand_weight:
        queries.append(create_query_by_ligand_weight(min_ligand_weight))

    if not queries:
        raise ValueError("At least one search criterion must be provided.")

    composite_query = rcsb.CompositeQuery(queries, "and")
    return rcsb.search(composite_query)


@redo.retriable(attempts=10, sleeptime=2)
def fetch_pdb_metadata(pdb_id: str) -> Dict:
    """
    Retrieve metadata for a specific PDB ID with retries.

    Args:
        pdb_id (str): PDB ID.

    Returns:
        Dict: Metadata dictionary.

    Raises:
        ValueError: If metadata retrieval fails.
    """
    metadata = pypdb.describe_pdb(pdb_id)
    if metadata is None:
        raise ValueError(f"Failed to fetch metadata for PDB ID: {pdb_id}")
    return metadata


def fetch_multiple_pdb_metadata(pdb_ids: List[str]) -> List[Dict]:
    """
    Retrieve metadata for multiple PDB IDs with retries.

    Args:
        pdb_ids (List[str]): List of PDB IDs.

    Returns:
        List[Dict]: List of metadata dictionaries.
    """
    return [fetch_pdb_metadata(pdb_id) for pdb_id in tqdm(pdb_ids)]


def retrieve_ligand_data(pdb_id: str) -> Dict[str, Dict]:
    """
    Fetch ligand data for a given PDB ID.

    Args:
        pdb_id (str): PDB ID.

    Returns:
        Dict[str, Dict]: Ligand data mapped by ligand ID.

    Raises:
        requests.RequestException: If fetching data fails.
    """
    pdb_info = _fetch_pdb_nonpolymer_info(pdb_id)
    ligand_ids = [
        entity["pdbx_entity_nonpoly"]["comp_id"]
        for entity in pdb_info["data"]["entry"]["nonpolymer_entities"]
    ]
    return {
        ligand_id: _fetch_ligand_info(ligand_id)
        for ligand_id in ligand_ids
    }


def _fetch_pdb_nonpolymer_info(pdb_id: str) -> Dict:
    """
    Fetch non-polymer entity information for a PDB ID using GraphQL.

    Args:
        pdb_id (str): PDB ID.

    Returns:
        Dict: Non-polymer entity information.

    Raises:
        requests.RequestException: If the request fails.
    """
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
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def _fetch_ligand_info(ligand_id: str) -> Dict:
    """
    Fetch ligand information from the Ligand Expo database.

    Args:
        ligand_id (str): Ligand ID.

    Returns:
        Dict: Ligand information.

    Raises:
        requests.RequestException: If the request fails.
    """
    url = f"http://ligand-expo.rcsb.org/reports/{ligand_id[0]}/{ligand_id}/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html = BeautifulSoup(response.text, "html.parser")
    return {
        row.find_all("td")[0].text.strip(): row.find_all("td")[1].text.strip()
        for table in html.find_all("table")
        for row in table.find_all("tr")
        if len(row.find_all("td")) == 2
    }
