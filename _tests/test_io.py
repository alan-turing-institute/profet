import os.path
import pytest
import profet
import profet.command_line
from profet import Fetcher
from profet import alphafold
from profet import pdb
from collections import defaultdict
from contextlib import redirect_stdout
import re

ONLY_ALPHAFOLD = "F4HvG8"
ONLY_PDB = "7U6Q"
ONE_SIGNAL_PEPTIDE = "P61316"
NO_SIGNAL_PEPTIDE = "P21170"


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


def test_cache(tmpdir):
    cache = profet.cache.PDBFileCache(directory=tmpdir)

    filename = cache.path("4V5D", "cif")
    assert filename == os.path.join(tmpdir, "4v5d.cif")

    filename = cache.path("4V5D", "pdb")
    assert filename == os.path.join(tmpdir, "4v5d.pdb")

    cache["4V5D"] = ("pdb", "cif", "4V5D cif data")
    cache["1U2P"] = ("alphafold", "pdb", "1U2P pdb data")
    cache["1U2P"] = ("pdb", "cif", "1U2P cif data")

    assert len(cache.find("2J3K")) == 0
    assert len(cache.find("4V5D")) == 1
    assert len(cache.find("1U2P")) == 2

    assert "2J3K" not in cache
    assert "4v5d" in cache
    assert "1u2p" in cache

    filename = cache["4v5d"]
    assert filename == os.path.join(tmpdir, "4v5d.cif")

    with open(filename) as infile:
        text = infile.read()
        assert text == "4V5D cif data"

    filename = cache["1u2p"]
    assert filename == os.path.join(tmpdir, "1u2p.pdb")

    with open(filename) as infile:
        text = infile.read()
        assert text == "1U2P pdb data"

    items = defaultdict(list)
    for identifier, filename in cache.items():
        items[identifier].append(filename)

    assert len(items) == 2
    assert len(items["4v5d"]) == 1
    assert len(items["1u2p"]) == 2
    assert os.path.join(tmpdir, "4v5d.cif") in items["4v5d"]
    assert os.path.join(tmpdir, "1u2p.cif") in items["1u2p"]
    assert os.path.join(tmpdir, "1u2p.pdb") in items["1u2p"]


def test_cache_download_cif_and_pdb(tmpdir):
    fetcher = profet.Fetcher()
    fetcher.set_directory(str(tmpdir))

    fetcher.get_file(
        uniprot_id="P0A855", filetype="cif", filesave=True, db="alphafold"
    )

    fetcher.get_file(
        uniprot_id="P0A855", filetype="pdb", filesave=True, db="alphafold"
    )

    assert os.path.exists(os.path.join(tmpdir, "p0a855.cif"))
    assert os.path.exists(os.path.join(tmpdir, "p0a855.pdb"))

    items = defaultdict(list)
    for identifier, filename in fetcher.cache().items():
        items[identifier].append(filename)
    assert len(items["p0a855"]) == 2


@pytest.mark.parametrize("test_id", get_test_ids())
def test_command_line_main(tmpdir, test_id):
    source, pdb_id = test_id

    with open("tmp.out", "w") as outfile:
        with redirect_stdout(outfile):
            profet.command_line.main(
                [pdb_id, "--save_directory", str(tmpdir), "--main_db", source]
            )
    with open("tmp.out") as infile:
        lines = list(infile.readlines())
        _, filename, _ = lines[-1].split("'")
        assert os.path.exists(filename)


@pytest.mark.parametrize(
    "signal_peptides, hydrogens, water, hetatoms, expected_filename_suffix",
    [
        (True, True, True, True, "nosignal1to25_nohydrogens_nowater_nohetatm"),
        (False, True, True, True, "nohydrogens_nowater_nohetatm"),
        (True, False, True, True, "nosignal1to25_nowater_nohetatm"),
        (True, True, False, True, "nosignal1to25_nohydrogens_nohetatm"),
        (True, True, True, False, "nosignal1to25_nohydrogens_nowater"),
        (
            False,
            False,
            False,
            False,
            "unmodified",
        ),
    ],
)
def test_fetcher_remove_stuff(
    tmpdir,
    signal_peptides,
    hydrogens,
    water,
    hetatoms,
    expected_filename_suffix,
):
    fetcher = Fetcher()
    fetcher.set_directory(str(tmpdir))

    # Fetch the file
    fetcher.get_file(
        uniprot_id="P45523", filetype="pdb", filesave=True, db="pdb"
    )

    # Remove elements based on the test parameters
    fetcher.remove(
        "P45523",
        signal_peptides=signal_peptides,
        hydrogens=hydrogens,
        water=water,
        hetatoms=hetatoms,
    )

    # Construct the expected filename
    expected_filename = os.path.join(
        str(tmpdir), f"p45523_1q6u_{expected_filename_suffix}.pdb"
    )

    # Assert that the expected file exists
    assert os.path.exists(expected_filename)
