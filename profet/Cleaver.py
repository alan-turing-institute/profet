import requests
import xml.etree.ElementTree as ET
import os


class Cleaver:
    """
    Class, identifying signal peptides based on UniProt and cleaving pdb/cif file to remove signal peptides of the
    protein structure.
    """

    def __init__(self):
        pass

    def signal_residuenumbers_requester(self, uniprot_id: str) -> list:
        """
        Collects all residue positions of the signal peptides to cleave.

        Args:
            uniprot_id: ID from Uniprot

        Returns:
            The list of the pairs of starting and end position in number of amino acids of the signal peptides given
            by UniProt.

        """
        # UniProt link to parse from
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.xml"
        # Send an HTTP GET request to the UniProt website
        response = requests.get(url)
        # Parse the XML content from the response
        root = ET.fromstring(response.content)
        # List to store multiple signal peptides
        signal_peptides = []

        # Find the signal peptide starting and end positions
        for child in root:
            for grandchild in child:
                if grandchild.attrib.get("type") == "signal peptide":
                    if (
                        grandchild[0][0].attrib.get("position")
                        and grandchild[0][1].attrib.get("position") is not None
                    ):
                        start_position = int(
                            str(grandchild[0][0].attrib.get("position"))
                        )
                        end_position = int(
                            str(grandchild[0][1].attrib.get("position"))
                        )
                        signal_peptides.append((start_position, end_position))
                    else:
                        print(uniprot_id + "has no signal peptide")
                else:
                    None
        return signal_peptides

    def remove_signal_peptide_pdb(
        self,
        pdb_file: str,
        signal_peptides: list,
        output_filename: str,
    ):
        """
        Load the pdb file and deletes the signal peptides. Save as new cleaved pdb file.

        Args:
            pdb_file: Path to the pdb input file
            signal_peptides: List of signal peptide start and ending positions pairs
            output_filename: Name of the cleaved protein file you want to write to
        Returns:
            None
        """

        with open(pdb_file, "r") as input_pdb:
            with open(output_filename, "w") as output_pdb:
                for line in input_pdb:
                    if line.startswith("ATOM"):
                        residue_position = int(
                            line[22:26].strip()
                        )  # 22-26 to check for amino acid number/ residue number
                        for start_position, end_position in signal_peptides:
                            if (
                                start_position
                                <= residue_position
                                <= end_position
                            ):
                                break
                        else:
                            output_pdb.write(line)
                    else:
                        output_pdb.write(line)

    def remove_signal_peptide_cif(
        self,
        input_file: str,
        signal_peptides: list,
        output_filename: str,
    ):
        """
        Load the cif file and deletes the signal peptides. Save as new cleaved cif file.

        Args:
            input_file: Path to the cif input file
            signal_peptides: List of signal peptide start end ending positions pairs
            output_filename: Name of the cleaved protein file you want to write to
        Returns:
            None
        """

        with open(input_file, "r") as infile, open(
            output_filename, "w"
        ) as outfile:
            for line in infile:
                if line.startswith("ATOM"):
                    residue_number = int(line[26:30].strip())
                    for start_position, end_position in signal_peptides:
                        if start_position <= residue_number <= end_position:
                            break
                        else:
                            outfile.write(line)
                else:
                    outfile.write(line)

    def anamder_pdb(
        self,
        input_file: str,
        signal_peptides: list,
    ) -> str:
        """
        From the input pdb dir\filename, amends it into an output filename a la filename_cleaved_xz_etc.pdb.
        Where xz are the beginning and end positions of the signal peptide.

        Args:
            input_file: Path to the pdb input file
            signal_peptides: List of signal peptide start end ending positions pairs
        Returns:
            Amended filename: filename_cleaved_xz_etc.pdb
        """

        # Extract the base filename
        base_name = os.path.basename(input_file)
        # Extract the directory without the file name
        directory = os.path.dirname(input_file)
        # Extract signal peptide information
        if signal_peptides != []:
            signal_info = "_".join(
                [f"{start}to{end}" for start, end in signal_peptides]
            )
        else:
            signal_info = "none"
        # Creating the new filename
        new_name = f"{directory}/{os.path.splitext(base_name)[0]}_cleaved_{signal_info}.pdb"
        return new_name

    def anamder_cif(
        self,
        input_file: str,
        signal_peptides: list,
    ) -> str:
        """
        From the input cif dir\filename, amends it into an output filename a la filename_cleaved_xz_etc.cif.
        Where xz are the beginning and end positions of the signal peptide.

        Args:
            input_file: Path to the cif input file
            signal_peptides: List of signal peptide start end ending positions pairs
        Returns:
            Amended filename: filename_cleaved_xz_etc.cif
        """

        # Extract the base filename
        base_name = os.path.basename(input_file)
        # Extract the directory without the file name
        directory = os.path.dirname(input_file)
        # Extract signal peptide information
        if signal_peptides != []:
            signal_info = "_".join(
                [f"{start}to{end}" for start, end in signal_peptides]
            )
        else:
            signal_info = "none"
        # Mend the new filename
        new_name = f"{directory}/{os.path.splitext(base_name)[0]}_cleaved_{signal_info}.cif"

        return new_name
