from .alphafold import Alphafold_DB
from .pdb import PDB_DB
from .cache import PDBFileCache
import os


class Fetcher:
    """
    The main class in profet to fetch protein structures from the PDB and
    alphafold databases.

    """

    def __init__(self, main_db: str = "pdb", save_directory: str = None):
        """
        Initialise the fetcher

        """
        self.type = main_db
        self.pdb = PDB_DB()
        self.alpha = Alphafold_DB()
        self.search_results = {}  # type: ignore
        self.save_directory = save_directory

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
        db: str = "pdb",
    ) -> tuple:
        """
        Returns the file from the correspondent database.

        Args:
            uniprot_id: ID from Uniprot.
            filetype: File type to be retrieved: cif, pdb.
            db: database from which to retrieve the file.

        Returns:
            Tuple containing the filename and file from the database

        """
        if db == "pdb":
            filetype, filedata = self.pdb.get_pdb(
                prot_id,
                filetype=filetype,
            )
        elif db == "alphafold":
            filetype, filedata = self.alpha.get_pdb(
                prot_id,
                filetype=filetype,
            )
        else:
            raise RuntimeError("Unknown db: %s" % db)

        return filetype, filedata

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

        # Get the PDB cache
        cache = PDBFileCache(directory=self.save_directory)

        # If the file is already downloaded then use that, otherwise search in
        # the PDB or alphafold databases
        if uniprot_id in cache:
            filename = cache[uniprot_id]
            with open(filename) as infile:
                filedata = infile.read()
        else:
            self.search_results[uniprot_id] = self.check_db(uniprot_id)
            if len(self.search_results[uniprot_id]):
                if db in self.search_results[uniprot_id]:
                    print("Structure available on defaulted database: " + db)
                    filetype, filedata = self.file_from_db(
                        prot_id=uniprot_id,
                        filetype=filetype,
                        db=db,
                    )
                else:
                    for item in self.search_results[uniprot_id]:
                        print(
                            "Structure available in alternative database: "
                            + item
                        )
                        filetype, filedata = self.file_from_db(
                            prot_id=uniprot_id,
                            filetype=filetype,
                            db=item,
                        )
            else:
                raise RuntimeError(
                    "Structure %s not available on any database" % uniprot_id
                )

            # Optionally save the data
            if filesave:
                cache[uniprot_id] = (filetype, filedata)
                filename = cache[uniprot_id]
            else:
                filename = None

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
        self.save_directory = os.path.abspath(os.path.expanduser(new_dir))

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
