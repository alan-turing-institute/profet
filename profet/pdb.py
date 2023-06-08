import pypdb.clients.pdb.pdb_client
from pypdb.clients.search.search_client import perform_search
from pypdb.clients.search.search_client import ReturnType
from pypdb.clients.search.operators import text_operators
from pypdb.clients.pdb.pdb_client import PDBFileType


class PDB_DB:
    """
    A class to represent the PDB database

    """

    def __init__(self):
        """
        Initialise the PDB data base class

        """
        self.return_type = ReturnType.ENTRY
        self.results = []

    def check_structure(self, uniprot_id: str) -> bool:
        """
        Check if a protein is contained within the PDB

        Args:
            uniprot_id: The uniprot id of the protein

        Returns:
            Is the protein in the PDB (True/False)

        """
        search_operator = text_operators.DefaultOperator(value=uniprot_id)
        try:
            self.results = perform_search(search_operator, self.return_type)
            return True
        except ValueError:
            return False

    def get_pdb(
        self,
        uniprot_id: str,
        filetype: str = "pdb",
        filesave: bool = False,
        filedir: str = "default",
    ) -> tuple:
        """
        Returns pdb/cif as strings, saves to file if requested

        Args:
            uniprot_id: ID from Uniprot
            filetype: File type to be retrieved: cif, pdb
            filesave: Option to save into a file
            filedir: The directory to save the data

        Returns:
            Tuple containing the filename and file from the database

        """

        # Search for the protein if we have not already done so
        if not self.results:
            search_operator = text_operators.DefaultOperator(value=uniprot_id)
            self.results = perform_search(search_operator, self.return_type)

        # Try to get the PDB file
        pdb_id = self.results[0]
        filedata = pypdb.clients.pdb.pdb_client.get_pdb_file(
            pdb_id, PDBFileType(filetype), compression=True
        )

        # If we couldn't find the file toggle the filetype and try again
        if filedata is None:
            if filetype == "pdb":
                filetype = "cif"
            else:
                filetype = "pdb"
            filedata = pypdb.clients.pdb.pdb_client.get_pdb_file(
                pdb_id, PDBFileType(filetype), compression=True
            )

        # Update the filename
        filedir = filedir + "." + filetype

        # Optionally save the data to disk
        if filesave:
            open(filedir, "wb").write(filedata)

        # Return the filename and file contents
        return filedir, filedata
