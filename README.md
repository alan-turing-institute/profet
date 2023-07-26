# profet
A Python 3  **pro**tein structure **fet**cher. Retrieves the cif or pdb files from either the RCSB Protein Data Bank ([PDB](https://www.rcsb.org), using [pypdb](https://github.com/williamgilpin/pypdb)) or [Alphafold](http://alphafold.ebi.ac.uk/) using the [Uniprot](http://uniprot.org/) ID. 

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![PyPI version shields.io](https://img.shields.io/pypi/v/profet.svg)](https://pypi.python.org/pypi/profet/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/python-profet.svg)](https://pypi.python.org/pypi/profet/)

[![Building](https://github.com/alan-turing-institute/profet/actions/workflows/python-package.yml/badge.svg)](https://github.com/alan-turing-institute/profet/actions/workflows/python-package.yml)
[![Publishing](https://github.com/alan-turing-institute/profet/actions/workflows/python-publish.yml/badge.svg)](https://github.com/alan-turing-institute/profet/actions/workflows/python-publish.yml)
[![Documentation](https://github.com/alan-turing-institute/profet/actions/workflows/sphinx.yml/badge.svg)](https://github.com/alan-turing-institute/profet/actions/workflows/sphinx.yml)

### Dependencies

Please install the latest version of PyPDB using:

```sh
pip install pypdb
```

or

```sh
pip install git+git://github.com/williamgilpin/pypdb
```

### Installation

Install `profet` using pip:

```sh
pip install profet
```

To install the development version, which contains the latest features and fixes, install directly from GitHub using

```sh
pip install git+git://github.com/alan-turing-institute/profet
```

Test the installation, navigate to the root directory and run

```sh
pytest
```

This code has been designed and tested for Python 3.

### Usage

This package can be used to retrieve the available protein structure from any Uniprot ID. 

The `Fetcher` class can search the IDs in both PDB and Alphafold, and saves the search results in a dictionary.

`get_file` returns the structure corresponding to `uniprot_id` in the defined `filetype:` (default as `'pdb'`, option as `'cif'`), searching first in the defaulted database `db` (default as `'pdb'`, option as `'alphafold'`).
The files can be saved to a local file with `filesave`.

`set_default_db` changes the default database into the given one between `'pdb'` and `'alphafold'`.

`set_directory` changes the directory where the files are saved. Files save as `<directory>/<id>.<filetype>`.

Run `search_history()` to see the search history of the fetcher.

#### Example usage:

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

Loads Profet and the file-fetcher, then specifies a directory to save the files at.
Lastly, downloads the protein with uniprod ID "P61316", in pdb format from the Alphafold databank and saves it in the specified directory.

For more detailed examples consult the following [Python notebook](./run_profet.ipynb).

### Documentation

You can find more documentation including a description of the python api [here](https://alan-turing-institute.github.io/profet/).

### Issues and Feature Requests

If you run into an issue, or if you find a workaround for an existing issue, we would very much appreciate it if you could post your question or code as a [GitHub issue](https://github.com/alan-turing-institute/profet/issues). 

### Contributions

If you would like to help contribute to profet, please read our [contribution](CONTRIBUTING.md) guide and [code of conduct](CODE_OF_CONDUCT.md).

