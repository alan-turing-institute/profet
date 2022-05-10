from .alphafold import Alphafold_DB
from .pdb import PDB_DB


class Fetcher:
    def __init__(self, main_db: str = 'pdb'):
        self.type = main_db
        self.pdb = PDB_DB()
        self.alpha = Alphafold_DB()
        self.search_results = {}
        self.save_directory = ""

    def check_db(self, uniprot_id: str):
        """ Checks which database contain the searched ID.
        Input:
        uniprot_id: str, ID from Uniprot
        Output:
        available_db: list of the databases where the id is available
        """

        available_db = []
        if self.pdb.check_structure(uniprot_id):
            available_db.append('pdb')
        if self.alpha.check_structure(uniprot_id):
            available_db.append('alphafold')
        return available_db

    def file_from_db(self, prot_id: str, filetype: str = 'pdb', filesave: bool = False, db: str = 'pdb'):
        """
        Returns the file from the correspondent database.
            Input:
                uniprot_id: str, ID from Uniprot
                filetype: str, File type to be retrieved: cif, pdb
                filesave: bool, Option to save into a file
                db: str, database from which to retrieve the file
            Output:
                File from the database
        """
        save_dir = self.save_directory + prot_id
        if db == 'pdb':
            return save_dir, self.pdb.get_pdb(prot_id, filetype=filetype, file_save=filesave, file_dir=save_dir)
        elif db == 'alphafold':
            return save_dir, self.alpha.get_pdb(prot_id, filetype=filetype, file_save=filesave, file_dir=save_dir)

    def get_file(self, uniprot_id: str, filetype: str = 'pdb', filesave: bool = False, db: str = 'pdb'):
        """
        Returns the file from an available database, starting with the defaulted that the user provided.
            Input:
                uniprot_id: str, ID from Uniprot
                filetype: str, File type to be retrieved: cif, pdb
                filesave: bool, Option to save into a file
                db: str, database from which to retrieve the file
            Output:
                File name of the saved file
                File from the database, or None if it is not available in any database.
        """
        self.search_results[uniprot_id] = self.check_db(uniprot_id)
        if len(self.search_results[uniprot_id]):
            if db in self.search_results[uniprot_id]:
                print("Structure available on defaulted database: "+db)
                filename, file = self.file_from_db(prot_id=uniprot_id, filetype=filetype, filesave=filesave, db=db)
                return filename, file
            else:
                for item in self.search_results[uniprot_id]:
                    print("Structure available on alternative database: "+item)
                    filename, file = self.file_from_db(prot_id=uniprot_id, filetype=filetype, filesave=filesave, db=db)
                    return filename, file
        else:
            print("Structure not available on any database")
            return None, None

    def search_history(self):
        """ Print the search history of the fetcher. """
        print(self.search_results)

    def set_directory(self, new_dir: str):
        """ Set the saving directory """
        if not new_dir.endswith("/"):
            new_dir = new_dir + "/"
        self.save_directory = new_dir

    def get_default_db(self):
        """ Return the default database."""
        return self.type

    def set_default_db(self, db: str):
        """ Set the default database"""
        if db in ['pdb', 'alphafold']:
            self.type = db
        else:
            print("Database not available.")
