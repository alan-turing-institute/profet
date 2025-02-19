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

    def remove_nonmain(
        self,
        input_file: str,
        signal_list: list = None,
        signal_peptides=True,
        hydrogens=True,
        water=True,
        hetatoms=True,
        output_filename: str = None,
    ):
        """
        Removes signal peptides, hydrogens, water molecules, and HETATM entries based on the flags passed.

        Args:
            input_file: Path to the input file (pdb or cif)
            signal_list: list of signal peptides to remove
            signal_peptides: Whether to remove signal peptides (default: True)
            hydrogens: Whether to remove hydrogens (default: True)
            water: Whether to remove water molecules (default: True)
            hetatoms: Whether to remove HETATM entries (default: True)
            output_filename: Optional custom output filename.
        Returns:
            None
        """

        # Ensure signal_list is a list or an empty list if None
        if signal_list is None:
            signal_list = []

        # Create dynamic parts of the filename
        filename_parts = []
        if signal_peptides and signal_list:
            signal_info = "_".join(
                [f"{start}to{end}" for start, end in signal_list]
            )
            filename_parts.append(f"nosignal{signal_info}")
        if signal_peptides and not signal_list:
            signal_info = "none"
            filename_parts.append(f"nosignal{signal_info}")
        if hydrogens:
            filename_parts.append("nohydrogens")
        if water:
            filename_parts.append("nowater")
        if hetatoms:
            filename_parts.append("nohetatm")

        # Set default output filename if none is provided
        if output_filename is None:
            base_name, ext = os.path.splitext(input_file)
            filename_suffix = (
                "_".join(filename_parts) if filename_parts else "unmodified"
            )
            output_filename = f"{base_name}_{filename_suffix}{ext}"

        def is_hydrogen_pdb(line: str) -> bool:
            return (
                line.startswith("ATOM") or line.startswith("HETATM")
            ) and line[12:16].strip().startswith("H")

        def is_hydrogen_cif(line: str) -> bool:
            return line.startswith("ATOM") and " H" in line

        def is_water_pdb(line: str) -> bool:
            return (
                line.startswith("ATOM") or line.startswith("HETATM")
            ) and line[17:20].strip() == "HOH"

        def is_water_cif(line: str) -> bool:
            return (
                line.startswith("ATOM") or line.startswith("HETATM")
            ) and "HOH" in line

        def is_hetatm_pdb(line: str) -> bool:
            return line.startswith("HETATM")

        def is_hetatm_cif(line: str) -> bool:
            return "HETATM" in line

        # Determine file format based on extension
        file_extension = input_file.split(".")[-1].lower()

        with open(input_file, "r") as input_f:
            with open(output_filename, "w") as output_f:
                for line in input_f:
                    if file_extension == "pdb":
                        # 22-26 to check for amino acid number/ residue number
                        residue_position = (
                            int(line[22:26].strip())
                            if line.startswith("ATOM")
                            else None
                        )

                        if signal_peptides and residue_position is not None:
                            if any(
                                start <= residue_position <= end
                                for start, end in signal_list
                            ):
                                continue
                        if hydrogens and is_hydrogen_pdb(line):
                            continue
                        if water and is_water_pdb(line):
                            continue
                        if hetatoms and is_hetatm_pdb(line):
                            continue
                        output_f.write(line)

                    elif file_extension == "cif":
                        columns = line.split()
                        residue_number = (
                            int(columns[8]) if len(columns) > 8 else None
                        )

                        if signal_peptides:
                            if any(
                                start <= residue_number <= end
                                for start, end in signal_list
                            ):
                                continue
                        if hydrogens and is_hydrogen_cif(line):
                            continue
                        if water and is_water_cif(line):
                            continue
                        if hetatoms and is_hetatm_cif(line):
                            continue
                        output_f.write(line)

                    else:
                        raise ValueError(
                            "Unsupported file format. Only pdb and cif are supported."
                        )

        print(f"File saved as {output_filename}")
