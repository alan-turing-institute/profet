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

        with open(input_file, "r") as infile:
            with open(output_filename, "w") as outfile:
                for line in infile:
                    if not signal_peptides:
                        outfile.write(line)
                    else:
                        if line.startswith("ATOM"):
                            # Split the line into columns based on whitespace
                            columns = line.split()
                            try:
                                residue_number = int(columns[8])
                            except ValueError as e:
                                print(f"Error converting to int: {e}")
                                # Handle the error or raise it again if needed

                            for start_position, end_position in signal_peptides:
                                if (
                                    start_position
                                    <= residue_number
                                    <= end_position
                                ):
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


    def remove_hydrogens(
            self,
            input_file: str,
            output_filename: str = None,
    ):
        """
        Load a PDB or CIF file and delete all hydrogen atoms. Save as a new pdb or cif file.

        Args:
            input_file: Path to the input file (pdb or cif)
            output_filename: Name of the output file to save without hydrogens. If not provided, defaults to originalname_nohydrogens.pdb or originalname_nohydrogens.cif.
        Returns:
            None
        """
        def is_hydrogen_pdb(line: str) -> bool:
            return (line.startswith("ATOM") or line.startswith("HETATM")) and line[12:16].strip().startswith("H")

        def is_hydrogen_cif(line: str) -> bool:
            return line.startswith("ATOM") and " H" in line

        # Determine file format based on extension
        file_extension = input_file.split('.')[-1].lower()

        # If output_filename is not provided, create the default one
        if output_filename is None:
            base_name, ext = os.path.splitext(input_file)
            output_filename = f"{base_name}_nohydrogens{ext}"

        with open(input_file, "r") as input_f:
            with open(output_filename, "w") as output_f:
                for line in input_f:
                    if file_extension == "pdb":
                        if not is_hydrogen_pdb(line):
                            output_f.write(line)
                    elif file_extension == "cif":
                        if not is_hydrogen_cif(line):
                            output_f.write(line)
                    else:
                        raise ValueError("Unsupported file format. Only pdb and cif are supported.")


    def remove_water_atoms(
            self,
            input_file: str,
            output_filename: str = None,
    ):
        """
        Delete all water atoms from pdb or cif file and save as new file.

        Args:
            input_file: Path to the input file (pdb or cif)
            output_filename: Name of the output file to save without water atoms.
                             If not provided, defaults to originalname_nowater.pdb or originalname_nowater.cif.
        Returns:
            None
        """
        def is_water_pdb(line: str) -> bool:
            return (line.startswith("ATOM") or line.startswith("HETATM")) and line[17:20].strip() == "HOH"

        def is_water_cif(line: str) -> bool:
            return (line.startswith("ATOM") or line.startswith("HETATM")) and "HOH" in line

        # Determine file format based on extension
        file_extension = input_file.split('.')[-1].lower()

        # If output_filename is not provided, create the default one
        if output_filename is None:
            base_name, ext = os.path.splitext(input_file)
            output_filename = f"{base_name}_nowater{ext}"

        with open(input_file, "r") as input_f:
            with open(output_filename, "w") as output_f:
                for line in input_f:
                    if file_extension == "pdb":
                        if not is_water_pdb(line):
                            output_f.write(line)
                    elif file_extension == "cif":
                        if not is_water_cif(line):
                            output_f.write(line)
                    else:
                        raise ValueError("Unsupported file format. Only pdb and cif are supported.")

    def remove_hetatoms(
            self,
            input_file: str,
            output_filename: str = None,
    ):
        """
        Load a pdb or cif file and delete all HETATM lines and save as a new file.

        Args:
            input_file: Path to the input file (pdb or cif)
            output_filename: Name of the output file to save without HETATM entries.
                             If not provided, defaults to originalname_nohetatm.pdb or originalname_nohetatm.cif.
        Returns:
            None
        """

        def is_hetatm_pdb(line: str) -> bool:
            return line.startswith("HETATM")

        def is_hetatm_cif(line: str) -> bool:
            return "HETATM" in line

        # Determine file format based on extension
        file_extension = input_file.split('.')[-1].lower()

        # If output_filename is not provided, create the default one
        if output_filename is None:
            base_name, ext = os.path.splitext(input_file)
            output_filename = f"{base_name}_nohetatm{ext}"

        with open(input_file, "r") as input_f:
            with open(output_filename, "w") as output_f:
                for line in input_f:
                    if file_extension == "pdb":
                        if not is_hetatm_pdb(line):
                            output_f.write(line)
                    elif file_extension == "cif":
                        if not is_hetatm_cif(line):
                            output_f.write(line)
                    else:
                        raise ValueError("Unsupported file format. Only pdb and cif are supported.")