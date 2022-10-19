from profet import Fetcher
from profet import alphafold
from profet import pdb

ONLY_ALPHAFOLD = "F4HvG8"
ONLY_PDB = "7U6Q"


def test_create_default_fetcher():
    prot_fetcher = Fetcher()
    assert prot_fetcher.get_default_db() == "pdb"


def test_set_default_database():
    prot_fetcher = Fetcher()
    prot_fetcher.set_default_db("alphafold")
    assert prot_fetcher.get_default_db() == "alphafold"


def test_check_db_not_none():
    prot_fetcher = Fetcher()
    assert prot_fetcher.check_db(ONLY_ALPHAFOLD) is not None


def test_check_structure_in_pdb():
    pdb_db = pdb.PDB_DB()
    assert pdb_db.check_structure(ONLY_PDB) is True


def test_check_structure_in_alphafold():
    af_db = alphafold.Alphafold_DB()
    assert af_db.check_structure(ONLY_ALPHAFOLD) is True


def test_id_available_alphafold():
    prot_fetcher = Fetcher()
    prot_fetcher.get_file(ONLY_ALPHAFOLD)
    assert prot_fetcher.search_history()[ONLY_ALPHAFOLD] == ["alphafold"]


def test_id_available_pdb():
    prot_fetcher = Fetcher()
    prot_fetcher.get_file(ONLY_PDB)
    assert prot_fetcher.search_history()[ONLY_PDB] == ["pdb"]
