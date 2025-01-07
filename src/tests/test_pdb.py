import pytest
from unittest.mock import patch, MagicMock
import biotite.database.rcsb as rcsb
from caddkit.api.pdb import (
    query_by_uniprot_id,
    query_by_deposition_date,
    query_by_experimental_method,
    query_by_resolution,
    query_by_polymer_count,
    query_by_ligand_mw,
    search_pdb,
    describe_one_pdb_id,
    fetch_pdb_metadata,
    get_ligands,
    _fetch_pdb_nonpolymer_info,
    _fetch_ligand_expo_info
)

def test_query_by_uniprot_id():
    query = query_by_uniprot_id("P00533")
    assert query._field == "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession"
    assert query._value == "P00533"

    with pytest.raises(ValueError):
        query_by_uniprot_id("")


def test_query_by_deposition_date():
    query = query_by_deposition_date("2020-01-01")
    assert query._field == "rcsb_accession_info.deposit_date"
    assert query._value == "2020-01-01"

    with pytest.raises(ValueError):
        query_by_deposition_date("")


def test_query_by_experimental_method():
    query = query_by_experimental_method("X-RAY DIFFRACTION")
    assert query._field == "exptl.method"
    assert query._value == "X-RAY DIFFRACTION"

    with pytest.raises(ValueError):
        query_by_experimental_method("")


def test_query_by_resolution():
    query = query_by_resolution(2.5)
    assert query._field == "rcsb_entry_info.resolution_combined"
    assert query._value == 2.5

    with pytest.raises(ValueError):
        query_by_resolution(-1.0)


def test_query_by_polymer_count():
    query = query_by_polymer_count(4)
    assert query._field == "rcsb_entry_info.deposited_polymer_entity_instance_count"
    assert query._value == 4

    with pytest.raises(ValueError):
        query_by_polymer_count(-1)


def test_query_by_ligand_mw():
    query = query_by_ligand_mw(150.0)
    assert query._field == "chem_comp.formula_weight"
    assert query._mol_definition
    assert query._value == 150.0

    with pytest.raises(ValueError):
        query_by_ligand_mw(0)


@patch("biotite.database.rcsb.search")
def test_search_pdb(mock_search):
    mock_search.return_value = ["1ABC", "2DEF"]
    results = search_pdb(uniprot_id="P12345", max_resolution=2.0)
    assert results == ["1ABC", "2DEF"]
    assert mock_search.called

    with pytest.raises(ValueError):
        search_pdb()


# @patch("pypdb.describe_pdb")
# def test_describe_one_pdb_id(mock_describe):
#     mock_describe.return_value = {"mock": "data"}
#     result = describe_one_pdb_id("1ABC")
#     assert result == {"mock": "data"}

#     mock_describe.return_value = None
#     with pytest.raises(ValueError):
#         describe_one_pdb_id("1DEF")


# @patch("requests.get")
# def test_fetch_pdb_metadata(mock_get):
#     mock_get.return_value = MagicMock(json=MagicMock(return_value={"mock": "data"}))
#     pdb_ids = ["1ABC", "2DEF"]
#     metadata = fetch_pdb_metadata(pdb_ids)
#     assert len(metadata) == len(pdb_ids)


# @patch("requests.get")
# def test_get_ligands(mock_get):
#     mock_get.return_value = MagicMock(
#         json=MagicMock(
#             return_value={
#                 "data": {
#                     "entry": {
#                         "nonpolymer_entities": [
#                             {"pdbx_entity_nonpoly": {"comp_id": "LIG"}}
#                         ]
#                     }
#                 }
#             }
#         )
#     )

#     @patch("your_module._fetch_ligand_expo_info", return_value={"info": "details"})
#     def test_ligand_expo_info(mock_expo_info):
#         ligands = get_ligands("1ABC")
#         assert ligands == {"LIG": {"info": "details"}}


# def test_fetch_pdb_nonpolymer_info():
#     with patch("requests.get") as mock_get:
#         mock_get.return_value.json.return_value = {"mock": "data"}
#         result = _fetch_pdb_nonpolymer_info("1ABC")
#         assert result == {"mock": "data"}


# def test_fetch_ligand_expo_info():
#     with patch("requests.get") as mock_get:
#         mock_get.return_value.text = "<table><tr><td>Key</td><td>Value</td></tr></table>"
#         result = _fetch_ligand_expo_info("LIG")
#         assert result == {"Key": "Value"}
