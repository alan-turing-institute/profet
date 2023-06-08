class Example_DB:
    """
    An example class to represent a database

    """

    def __init__(self):
        """
        Initialise the database

        """
        pass

    def check_structure(self, uniprot_id: str) -> bool:
        """
        Check whether a structure is present in the database database

        Args:
            uniprot_id: The uniprot id of the protein

        Returns:
            Is the protein in the database (True/False)

        """
        raise RuntimeError("Not implemented")

    def get_pdb(
        self,
        uniprot_id: str,
        filetype: str = "pdb",
        filesave: bool = False,
        filedir: str = "default",
    ) -> tuple:
        """
        Returns pdb/cif as strings, saves to file if requested.

        Args:
            uniprot_id: ID from Uniprot
            filetype: File type to be retrieved: cif, pdb
            filesave: Option to save into a file
            filedir: The directory to save the data

        Returns:
            Tuple containing the filename and file from the database

        """
        raise RuntimeError("Not implemented")
