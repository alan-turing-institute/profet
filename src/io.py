"""
Order of things to do:
search if protein has hit in pdb
if yes, return the hits for the protein. what if more than one?
if no, return hits for the protein in alphafold w/ confidence interval.

Option: go straight to alphafold or to pdb
"""

from alphafold import Alphafold_DB
from pdb import PDB_DB

test_db = Alphafold_DB()

#test_db.get_file_url(uniprot_id="F4HvG8")

print(test_db.check_structure("F4HvG8"))