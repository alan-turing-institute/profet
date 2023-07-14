Usage
=====

This package can be used to retrieve the available protein structure from any
Uniprot ID. 

The :class:`profet.Fetcher` class can search the IDs in both PDB and Alphafold, and saves the
search results in a dictionary.

:meth:`profet.Fetcher.get_file` returns the structure corresponding to
`uniprot_id` in the defined `filetype:` (default as `'pdb'`, option as
`'cif'`), searching first in the defaulted database `db` (default as `'pdb'`,
option as `'alphafold'`).  The files can be saved to a local file with
`filesave`.

:meth:`profet.Fetcher.set_default_db` changes the default database into the
given one between `'pdb'` and `'alphafold'`.

:meth:`profet.Fetcher.set_directory` changes the directory where the files are
saved. Files save as `<directory>/<id>.<filetype>`.

Run :meth:`profet.Fetcher.search_history()` to see the search history of the fetcher.

See the run_profet.ipynb notebook for usage examples.
