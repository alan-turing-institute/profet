from typing import Optional
import os


class PDBFileCache(object):
    """
    A class to cache the PDB files

    """

    def __init__(self, directory: str = None):
        """
        Initialise the cache object with the directory

        If directory is None then the cache is set to ~/.cache/pdb

        Args:
            directory: The cache directory

        """

        # Set the cache directory
        self.directory = os.path.abspath(
            directory
            if directory is not None
            else os.path.abspath(
                os.path.expanduser(os.path.join("~", ".cache", "pdb"))
            )
        )

        # Create the directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

    def path(self, uniprot_id: str, filetype: str = "pdb") -> str:
        """
        Get the proposed path

        Args:
            uniprot_id: The uniprot id
            filetype: Either pdb or cif

        Returns:
            The absolute path

        """
        assert filetype in ["pdb", "cif"]
        return os.path.join(self.directory, uniprot_id.lower()) + "." + filetype

    def find(self, uniprot_id: str) -> list:
        """
        Find all items matching the uniprot_id

        Args:
            uniprot_id: The uniprot id

        Returns:
            The list of matching items

        """
        return [
            filename
            for filename in [
                self.path(uniprot_id, filetype) for filetype in ["pdb", "cif"]
            ]
            if os.path.exists(filename)
        ]

    def __contains__(self, uniprot_id: str) -> bool:
        """
        Check if the filename is in the cache

        Args:
            uniprot_id: The uniprot id

        Returns:
            True/False if the filename is in the cache

        """
        return len(self.find(uniprot_id)) > 0

    def __getitem__(self, uniprot_id: str) -> Optional[tuple]:
        """
        Get the full path to the item

        Args:
            uniprot_id: The uniprot id

        Returns:
            The absolute path to the item

        """
        if uniprot_id not in self:
            return None
        return self.find(uniprot_id)[0]

    def __setitem__(self, uniprot_id: str, item: tuple):
        """
        Write the file into the cache

        Args:
            uniprot_id: The uniprot id
            item: (The file type, The file data)

        """

        # Get the item components
        filetype, filedata = item

        # Bytes or string
        if isinstance(filedata, (bytes, bytearray)):
            mode = "wb"
        else:
            mode = "w"

        # Write the file
        with open(self.path(uniprot_id, filetype), mode) as outfile:
            outfile.write(filedata)

    def items(self):
        """
        Iterate through the items in the cache

        """
        for filename in os.listdir(self.directory):
            if filename.endswith(".cif") or filename.endswith(".pdb"):
                uniprot_id, filetype = os.path.splitext(filename)
                yield uniprot_id, self.path(uniprot_id, filetype)
