from .alphafold import Alphafold_DB
from .pdb import PDB_DB


class Fetcher:
    """
    The main class in profet to fetch protein structures from the PDB and
    alphafold databases.

    """

    def __init__(self, main_db: str = "pdb"):
        """
        Initialise the fetcher

        """
        self.type = main_db
        self.pdb = PDB_DB()
        self.alpha = Alphafold_DB()
        self.search_results = {}  # type: ignore
        self.save_directory = ""

    def check_db(self, uniprot_id: str) -> list:
        """
        Checks which database contains the searched ID.

        Args:
            uniprot_id: ID from Uniprot

        Returns:
            The list of the databases where the id is available

        """

        available_db = []
        if self.pdb.check_structure(uniprot_id):
            available_db.append("pdb")
        if self.alpha.check_structure(uniprot_id):
            available_db.append("alphafold")
        return available_db

    def file_from_db(
        self,
        prot_id: str,
        filetype: str = "pdb",
        filesave: bool = False,
        db: str = "pdb",
    ) -> tuple:
        """
        Returns the file from the correspondent database.

        Args:
            uniprot_id: ID from Uniprot.
            filetype: File type to be retrieved: cif, pdb.
            filesave: Option to save into a file.
            db: database from which to retrieve the file.

        Returns:
            Tuple containing the filename and file from the database

        """
        save_dir = self.save_directory + prot_id
        if db == "pdb":
            filename, filedata = self.pdb.get_pdb(
                prot_id,
                filetype=filetype,
                filesave=filesave,
                filedir=save_dir,
            )
        elif db == "alphafold":
            filename, filedata = self.alpha.get_pdb(
                prot_id,
                filetype=filetype,
                filesave=filesave,
                filedir=save_dir,
            )
        else:
            raise RuntimeError("Unknown db: %s" % db)

        return filename, filedata

    def get_file(
        self,
        uniprot_id: str,
        filetype: str = "pdb",
        filesave: bool = False,
        db: str = "pdb",
    ) -> tuple:
        """
        Returns the file from an available database, starting with the
        default that the user provided.

        Args:
            uniprot_id: ID from Uniprot.
            filetype: File type to be retrieved: cif, pdb.
            filesave: Option to save into a file.
            db: database from which to retrieve the file.

        Returns:
            A tuple containing:
            1. File name of the saved file
            2. File from the database, or None if it is not available in any database.

        """
        self.search_results[uniprot_id] = self.check_db(uniprot_id)
        if len(self.search_results[uniprot_id]):
            if db in self.search_results[uniprot_id]:
                print("Structure available on defaulted database: " + db)
                filename, filedata = self.file_from_db(
                    prot_id=uniprot_id,
                    filetype=filetype,
                    filesave=filesave,
                    db=db,
                )
            else:
                for item in self.search_results[uniprot_id]:
                    print(
                        "Structure available in alternative database: " + item
                    )
                    filename, filedata = self.file_from_db(
                        prot_id=uniprot_id,
                        filetype=filetype,
                        filesave=filesave,
                        db=item,
                    )
        else:
            raise RuntimeError(
                "Structure %s not available on any database" % uniprot_id
            )

        # Return the filename and file
        return filename, filedata

    def search_history(self) -> dict:
        """
        Returns:
            The search history of the fetcher.

        """
        return self.search_results

    def set_directory(self, new_dir: str):
        """
        Set the saving directory.

        Args:
            new_dir: The directory to save data

        """
        if not new_dir.endswith("/"):
            new_dir = new_dir + "/"
        self.save_directory = new_dir

    def get_default_db(self) -> str:
        """
        Returns:
            The default database.

        """
        return self.type

    def set_default_db(self, db: str):
        """
        Set the default database.

        Args:
            db: The default db (pdb or alphafold)

        """
        if db in ["pdb", "alphafold"]:
            self.type = db
        else:
            raise RuntimeError("Database not available: %s" % db)
