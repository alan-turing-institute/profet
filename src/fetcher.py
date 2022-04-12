from alphafold import Alphafold_DB
from pdb import PDB_DB


class Fetcher:
    def __init__(self, db_type: str = 'pdb'):
        self.type = db_type
        if self.type == 'pdb':
            self.db = PDB_DB()
        elif self.type == 'alphafold':
            self.db = Alphafold_DB()
        else:
            self.db = None
            print('No valid database type was provided.')

    def retrieve_pdb(self, pdb_id: str, filetype: str='pdb', filesave: bool=False):
        if self.db.check_structure(pdb_id):
            return self.db.get_pdb(pdb_id, filetype, filesave)
        else:
            return 'No pdb file available in the chosen database'