"""https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v2.cif
https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-model_v2.pdb
https://alphafold.ebi.ac.uk/files/AF-F4HVG8-F1-predicted_aligned_error_v2.json


read entry: https://alphafold.ebi.ac.uk/entry/F4HVG8
find cif, download that file"""
import pandas as pd
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup


class Alphafold_DB:

    def __init__(self):
        self.df = pd.read_csv("http://ftp.ebi.ac.uk/pub/databases/alphafold/accession_ids.txt",
                              names=["Uniprot_ID", "First_residue", "Last_residue", "AF_ID", "version"], encoding="iso-8859-1")
        self.session = HTMLSession()
        self.common_url = "https://alphafold.ebi.ac.uk/entry/"

    def check_structure(self, uniprot_id: str):
        """ Check whether a structure is present in AlphaFold database"""
        return self.df['Uniprot_ID'].eq(uniprot_id.upper()).any()

    def get_file_url(self, uniprot_id: str, filetype: str = "pdb"):
        """ Get file url relative to an id from the Alphafold entry page"""

        if filetype in ["pdb", "cif"]:
            uniprot_id = uniprot_id.upper()
            # Get the url with the id
            response = self.session.get(self.common_url + uniprot_id)

            # Render the javascript
            response.html.render()

            # Parse the rendered html
            soup = BeautifulSoup(response.html.html, "lxml")

            # Find url correspondent to the intended filetype
            url = soup.select_one("a[href*=" + filetype + "]")

            return url['href']
        else:
            return "Filetype not supported"

    def get_pdb(self, uniprot_id: str, filetype: str = "pdb", file_save: bool = False):
        """ Returns pdb/cif as strings, saves to file if requested """
        af_id = self.df.loc[self.df['Uniprot_ID'] == uniprot_id.upper()]["AF_ID"].to_numpy()[0]
        version = self.df.loc[self.df['Uniprot_ID'] == uniprot_id.upper()]["version"].to_numpy()[0]

        url = "https://alphafold.ebi.ac.uk/files/" + af_id + "-model_v" + str(version) + "." + filetype
        file = requests.get(url)
        print(url)
        if len(file.content) < 200:
            url = self.get_file_url(uniprot_id, filetype)
            file = requests.get(url)
        if file_save:
            open(file_save, 'wb').write(file.text)

        return file.text


