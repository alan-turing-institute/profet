from urllib.request import urlretrieve
from rcsbsearchapi import TextQuery


class PDB_DB:
    """
    A class to represent the PDB database

    """

    def __init__(self):
        """
        Initialise the PDB data base class

        """
        pass
        # self.return_type = ReturnType.ENTRY
        self.results = []

    def uniprot_id_to_pdb_id(self, uniprot_id: str):
        """
        Convert a uniprot_id to a pdb_id by selecting first entry

        Args:
            uniprot_id: The uniprot id of the protein

        Returns:
            The PDB id

        """
        query = TextQuery(value=uniprot_id)
        for result in query():
            return result
        return None

    def check_structure(self, uniprot_id: str) -> bool:
        """
        Check if a protein is contained within the PDB

        Args:
            uniprot_id: The uniprot id of the protein

        Returns:
            Is the protein in the PDB (True/False)

        """
        pdb_id = self.uniprot_id_to_pdb_id(uniprot_id)
        if pdb_id is not None:
            self.results = [pdb_id]
            return True
        return False

    def make_url(self, uniprot_id: str, filetype: str = "pdb") -> str:
        """
        Make the URL for the protein

        Args:
            uniprot_id: The uniprot id of the protein
            filetype: The type of file to download (pdb or cif)

        Returns:
            The URL of the file to download

        """

        uniprot_id = uniprot_id.upper()
        url = f"https://files.rcsb.org/download/{uniprot_id}.{filetype}"
        return url

    def get_pdb(
        self,
        uniprot_id: str,
        filetype: str = "pdb",
    ) -> tuple:
        """
        Returns pdb/cif as strings, saves to file if requested

        Args:
            uniprot_id: ID from Uniprot
            filetype: File type to be retrieved: cif, pdb

        Returns:
            Tuple containing the filename and file from the database

        """

        if not self.results:
            self.results = [self.uniprot_id_to_pdb_id(uniprot_id)]

        # Try to get the PDB file
        pdb_id = self.results[0]

        try:
            url = self.make_url(pdb_id, filetype)
            filename, result = urlretrieve(url)
            with open(filename) as file:
                filedata = file.read()
        except Exception:
            if filetype == "pdb":
                filetype = "cif"
            else:
                filetype = "pdb"
            url = self.make_url(pdb_id, filetype)
            filename, result = urlretrieve(url)
            with open(filename) as file:
                filedata = file.read()

        # If pdb is not the same then add the pdb id to the uniprot id as the identifier
        if pdb_id.lower() != uniprot_id.lower():
            identifier = uniprot_id + "_" + pdb_id
        else:
            identifier = uniprot_id

        # Return the identifier, file type and file contents
        return identifier, filetype, filedata
