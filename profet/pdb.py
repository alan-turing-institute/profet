import pypdb.clients.pdb.pdb_client
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators


class PDB_DB:
    def __init__(self):
        self.return_type = ReturnType.ENTRY
        self.results = []

    def check_structure(self, uniprot_id: str):
        search_operator = text_operators.DefaultOperator(value=uniprot_id)
        try:
            self.results = perform_search(search_operator, self.return_type)
            return True
        except ValueError:
            return False

    def get_pdb(self, uniprot_id: str, filetype: str = "pdb", file_save: bool = False, file_dir: str = "default"):
        if not self.results:
            search_operator = text_operators.DefaultOperator(value=uniprot_id)
            self.results = perform_search(search_operator, self.return_type)

        pdb_id = self.results[0]
        pdb_file = pypdb.clients.pdb.pdb_client.get_pdb_file(pdb_id, filetype)
        if pdb_file is None:
            if filetype == "pdb":
                filetype = "cif"
            else:
                filetype = "pdb"
            pdb_file = pypdb.clients.pdb.pdb_client.get_pdb_file(pdb_id, filetype)
        file_dir = file_dir + "." + filetype
        if file_save:
            open(file_dir, 'wb').write(pdb_file)

        return pdb_file
