"""
Order of things to do:
search if protein has hit in pdb
if yes, return the hits for the protein. what if more than one?
if no, return hits for the protein in alphafold w/ confidence interval.

Option: go straight to alphafold or to pdb
"""
from profet import Fetcher

ONLY_ALPHAFOLD = "F4HvG8"
ONLY_PDB = ""


def test_create_default_fetcher():
    prot_fetcher = Fetcher()
    assert prot_fetcher.get_default_db() == 'pdb'


def test_set_default_database():
    prot_fetcher = Fetcher()
    prot_fetcher.set_default_db('alphafold')
    assert prot_fetcher.get_default_db() == 'alphafold'


def test_id_available_alphafold():
    prot_fetcher = Fetcher()
    prot_fetcher.get_file(ONLY_ALPHAFOLD)
    assert prot_fetcher.search_history()[ONLY_ALPHAFOLD] == ["alphafold"]


def test_id_available_pdb():
    prot_fetcher = Fetcher()
    prot_fetcher.get_file(ONLY_PDB)
    assert prot_fetcher.search_history()[ONLY_PDB] == ["pdb"]
