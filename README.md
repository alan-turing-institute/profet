# profet
A Python 3  **pro**tein structure **fet**cher. Retrieves the cif or pdb files from either the RCSB Protein Data Bank ([PDB](https://www.rcsb.org), using [pypdb](https://github.com/williamgilpin/pypdb)) or [Alphafold](http://alphafold.ebi.ac.uk/) using the [Uniprot](http://uniprot.org/) ID. 

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![PyPI version shields.io](https://img.shields.io/pypi/v/profet.svg)](https://pypi.python.org/pypi/profet/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/profet.svg)](https://pypi.python.org/pypi/profet/)

[![Building](https://github.com/alan-turing-institute/profet/actions/workflows/python-package.yml/badge.svg)](https://github.com/alan-turing-institute/profet/actions/workflows/python-package.yml)
[![Publishing](https://github.com/alan-turing-institute/profet/actions/workflows/python-publish.yml/badge.svg)](https://github.com/alan-turing-institute/profet/actions/workflows/python-publish.yml)
[![Documentation](https://github.com/alan-turing-institute/profet/actions/workflows/sphinx.yml/badge.svg)](https://github.com/alan-turing-institute/profet/actions/workflows/sphinx.yml)

## Dependencies

Please install the latest version of PyPDB using:

```sh
pip install pypdb
```

or

```sh
pip install git+git://github.com/williamgilpin/pypdb
```

## Installation

### For users

Install `profet` using pip:

```sh
pip install profet
```

### For developers

To install the development version, which contains the latest features and fixes, install directly from GitHub using:

```sh
pip install git+git://github.com/alan-turing-institute/profet
```

To test the installation, you need to have pytest and pytest-cov packagages installed which can be done as follows.

```sh
pip install pytest pytest-cov
```

Then navigate to the root directory of the package and run

```sh
pytest
```

This code has been designed and tested for Python 3.

## Usage

This package can be used to retrieve the available protein structure from any Uniprot ID. It can also be used to automatically delete signal peptides off the structure.

### Python API Usage

The `Fetcher` class can search the IDs in both PDB and Alphafold, and saves the search results in a dictionary.

`get_file` returns the structure corresponding to `uniprot_id` in the defined `filetype:` (default as `'pdb'`, option as `'cif'`), searching first in the defaulted database `db` (default as `'pdb'`, option as `'alphafold'`).
The files can be saved to a local file with `filesave`: the files are saved as `uniprotID.<filetype>`, except when the files are fetched from PDB and, in that case, are saved as `uniprotID_pdbID.<filetype>`.

`set_default_db` changes the default database into the given one between `'pdb'` and `'alphafold'`.

`set_directory` changes the directory where the files are saved. Files save as `<directory>/<id>.<filetype>`.

Run `search_history()` to see the search history of the fetcher.

#### Example:

```python
import profet as pf
fetcher = pf.Fetcher()
fetcher.set_directory("/path/to/directory/folder")
fetcher.get_file(uniprot_id = "P61316", filetype = "pdb", filesave = True, db = "alphafold")

fetcher.search_history()
```

returns:
```
{'P61316': ['pdb', 'alphafold']}
```

Loads `profet` and the file-fetcher, then specifies a directory to save the files at.
Lastly, downloads the protein with uniprod ID "P61316", in pdb format from the Alphafold databank and saves it in the specified directory.

For more detailed examples consult the following [Python notebook](./run_profet.ipynb).

### Signal Peptide Cleaving Usage

Once a structure is downloaded using `get_file`, the signal cleaving function `cleave_off_signal_peptides` from the `Fetcher` class, compares the sequence of the structure to the UniProt database for any signal peptides included in the structure. It then automatically deletes the signal peptides from the structure.
The cleaved structure is saved as a separate file, with the deleted residue positions added to the filename. In the case of no signal peptides being detected, as new file named "structure-ID_None.cif/.pdb" will be saved.

#### Example:

```python
import profet as pf
fetcher = pf.Fetcher()
fetcher.set_directory("/path/to/directory/folder")
fetcher.get_file(uniprot_id = "P0A855", filetype = "pdb", filesave = True, db = "alphafold")
fetcher.cleave_off_signal_peptides("P0A855")
```
This will save p0a855.pdb and p0a855_cleaved_1to21.pdb to the specified directory.

### Command Line Usage

The `profet` library also has a command line interface that mirrors the python
API and which can be used to download entries from both the PDB and AlphaFold.
An example of how to use the profet command line program is shown in the
following code snippet.

```bash
profet 4v1w \
  --filetype=pdb \
  --main_db=pdb \
  --save_directory="~/.pdb"
```

In this example, the entry "4V1W" is to be downloaded from the PDB database as
a .pdb file. The file will be cached in the "~/.pdb" directory for future use.

## Documentation

You can find more documentation including a description of the python api [here](https://alan-turing-institute.github.io/profet/).

## Issues and Feature Requests

If you run into an issue, or if you find a workaround for an existing issue, we would very much appreciate it if you could post your question or code as a [GitHub issue](https://github.com/alan-turing-institute/profet/issues). 

## Contributions

If you would like to help contribute to `profet`, please read our [contribution](CONTRIBUTING.md) guide and [code of conduct](CODE_OF_CONDUCT.md).

