# profet
A Python 3  **pro**tein structure **fet**cher. Retrieves the cif or pdb files from either the RCSB Protein Data Bank ([PDB](https://www.rcsb.org), using [pypdb](https://github.com/williamgilpin/pypdb)) or [Alphafold](http://alphafold.ebi.ac.uk/) using the [Uniprot](http://uniprot.org/) ID. 

[![Building](https://github.com/jmp1985/profet/actions/workflows/python-package.yml/badge.svg)](https://github.com/jmp1985/profet/actions/workflows/python-package.yml)

### Dependencies

Please install the latest version of PyPDB using:

`$ pip install git+git://github.com/williamgilpin/pypdb`

### Installation

Install `profet` using pip:

`$ pip install profet`

To install the development version, which contains the latest features and fixes, install directly from GitHub using

`$ pip install git+git://github.com/alan-turing-institute/profet`

Test the installation, navigate to the root directory and run

`$ pytest `

This code has been designed and tested for Python 3.

### Usage

This package can be used to retrieve the available protein structure from any Uniprot ID. 

The `Fetcher` class can search the IDs in both PDB and Alphafold, and saves the search results in a dictionary.

`get_file` returns the structure corresponding to `uniprot_id` in the defined `filetype:` (default as `'pdb'`, option as `'cif'`), searching first in the defaulted database `db` (default as `'pdb'`, option as `'alphafold'`).
The files can be saved to a local file with `filesave`.

`set_default_db` changes the default database into the given one between `'pdb'` and `'alphafold'`.

`set_directory` changes the directory where the files are saved. Files save as `<directory>/<id>.<filetype>`.

Run `search_history()` to see the search history of the fetcher.

### Issues and Feature Requests
If you run into an issue, or if you find a workaround for an existing issue, we would very much appreciate it if you could post your question or code as a [GitHub issue](https://github.com/alan-turing-institute/profet/issues).

