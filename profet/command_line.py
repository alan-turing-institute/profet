from argparse import ArgumentParser
from profet import Fetcher
from typing import List
import os


__all__ = ["main"]


def get_description():
    """
    Get the program description

    """
    return "Download a PDB file"


def get_parser(parser: ArgumentParser = None) -> ArgumentParser:
    """
    Get the parser for the command line

    """

    # Initialise the parser
    if parser is None:
        parser = ArgumentParser(description=get_description())

    # Add some command line arguments
    parser.add_argument(
        "uniprot_id",
        type=str,
        nargs="+",
        help="The uniprot_ids of the files to collect",
    )
    parser.add_argument(
        "--filetype",
        type=str,
        dest="filetype",
        default="cif",
        choices=["pdb", "cif"],
        help="The file type to download",
    )
    parser.add_argument(
        "--main_db",
        type=str,
        default="pdb",
        dest="main_db",
        choices=["pdb", "alphafold"],
        help="The yaml file to configure the simulation",
    )

    parser.add_argument(
        "--save_directory",
        type=str,
        default=os.path.abspath(os.path.expanduser("~/.cache/pdb")),
        dest="save_directory",
        help="The directory to save the PDB files.",
    )

    return parser


def main_impl(args):
    """
    Use profet to download some PDB files

    """

    # Create the fetcher
    fetcher = Fetcher(main_db=args.main_db, save_directory=args.save_directory)

    # Get the file
    for identifier in args.uniprot_id:
        filename, filedata = fetcher.get_file(
            identifier, filetype=args.filetype, filesave=True, db=args.main_db
        )
        print("Saved %s to '%s'" % (identifier, filename))


def main(args: List[str] = None):
    """
    Create a main configuration

    """
    main_impl(get_parser().parse_args(args=args))
