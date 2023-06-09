"""https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v2.cif
https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v2.pdb
https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-predicted_aligned_error_v2.json


read entry: https://alphafold.ebi.ac.uk/entry/F4HVG8
find cif, download that file"""
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup


class Alphafold_DB:
    """
    A class to represent the Alphafold database

    """

    def __init__(self):
        """
        Initialise the Alphafold data base class

        """
        # self.df = pd.read_csv("http://ftp.ebi.ac.uk/pub/databases/alphafold/accession_ids.csv",
        #                      names=["Uniprot_ID", "First_residue", "Last_residue", "AF_ID", "version"], encoding="iso-8859-1")
        self.df = None
        self.session = HTMLSession()
        self.common_url = "https://alphafold.ebi.ac.uk/entry/"

    def check_structure(self, uniprot_id: str) -> bool:
        """
        Check whether a structure is present in the AlphaFold database

        Args:
            uniprot_id: The uniprot id of the protein

        Returns:
            Is the protein in the Alphafold database (True/False)

        """
        uniprot_id = uniprot_id.upper()
        url = self.make_url(uniprot_id, "pdb")
        r = requests.get(url)
        return r.status_code != 404

    def get_file_url(self, uniprot_id: str, filetype: str = "pdb") -> str:
        """
        Get file url relative to an id from the the Alphafold entry page

        Args:
            uniprot_id: The uniprot id of the protein
            filetype: The type of file to download (pdb or cif)

        Returns:
            The URL of the file to download

        """

        # Do we recognise the filetpye, otherwise raise an exception.
        if filetype in ["pdb", "cif"]:
            uniprot_id = uniprot_id.upper()
            # Get the url with the id.
            response = self.session.get(self.common_url + uniprot_id)

            # Render the javascript.
            response.html.render()

            # Parse the rendered html.
            soup = BeautifulSoup(response.html.html, "lxml")

            # Find url correspondent to the intended filetype.
            url = soup.select_one("a[href*=" + filetype + "]")
        else:
            raise RuntimeError("Filetype not supported: %s" % filetype)

        # Return the URL
        return url["href"]

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
        af_id = "AF-" + uniprot_id + "-F1"

        # https: // alphafold.ebi.ac.uk / files / AF - A0A6J1BG53 - F1 - model_v3.pdb
        version = 3
        url = (
            "https://alphafold.ebi.ac.uk/files/"
            + af_id
            + "-model_v"
            + str(version)
            + "."
            + filetype
        )

        return url

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
        # af_id = self.df.loc[self.df['Uniprot_ID'] == uniprot_id.upper()]["AF_ID"].to_numpy()[0]
        # version = self.df.loc[self.df['Uniprot_ID'] == uniprot_id.upper()]["version"].to_numpy()[0]
        # af_id = "AF-"+uniprot_id+"-F1"

        # https: // alphafold.ebi.ac.uk / files / AF - A0A6J1BG53 - F1 - model_v3.pdb
        # version = 3
        # url = "https://alphafold.ebi.ac.uk/files/" + af_id + "-model_v" + str(version) + "." + filetype

        # Make the URL
        url = self.make_url(uniprot_id, filetype)

        # Perform the HTML request to get the file
        file = requests.get(url)
        if len(file.content) < 200:
            url = self.get_file_url(uniprot_id, filetype)
            file = requests.get(url)

        # Update the filename
        filedir = filedir + "." + filetype

        # Optionally save the data to disk
        if filesave:
            open(filedir, "w").write(file.text)

        # Return the filename and file contents
        return filedir, file.text
