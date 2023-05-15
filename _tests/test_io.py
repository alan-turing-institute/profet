import os.path
import pytest
import profet
from profet import Fetcher
from profet import alphafold
from profet import pdb

ONLY_ALPHAFOLD = "F4HvG8"
ONLY_PDB = "7U6Q"


def get_test_ids():
    test_id_map = {"alphafold": ["F4HvG8"], "pdb": ["4V5D", "6Z6U", "7U6Q"]}

    for source, test_id_list in test_id_map.items():
        for test_id in test_id_list:
            yield source, test_id


def test_version():
    version = profet.__version__
    assert version != "unknown"


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


@pytest.mark.parametrize("test_id", get_test_ids())
def test_fetcher_get_file(tmpdir, test_id):
    source, pdb_id = test_id
    fetcher = Fetcher(source)
    fetcher.set_directory(str(tmpdir))
    filename, contents = fetcher.get_file(pdb_id, filesave=True)
    assert os.path.exists(filename)
