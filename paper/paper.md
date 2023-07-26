---
title: '*profet*: A Python package to download PDBs from different sources'
tags:
  - Python
  - protein structures
authors:
  - name: Beatriz Costa-Gomes
    orcid: 0000-0002-1073-8442
    affiliation: 1
    corresponding: true
  - name: James Parkhurst
    orcid: 0000-0002-9120-8354
    affiliation: "2,3"
  - name: Nikolai Juraschko
    orcid: 0000-0001-6748-1716
    affiliation: "2,4"
  - name: Mark Basham
    orcid: 0000-0002-8438-1415
    affiliation: 2
  - name: Alan Lowe
    orcid: 0000-0002-0558-3597 
    affiliation: "1,5"  
affiliations:
 - name: The Alan Turing Institute, UK
   index: 1
 - name: Rosalind Franklin Institute, UK
   index: 2
 - name: Diamond Light Source, UK
   index: 3
 - name: University of Oxford, UK
   index: 4
 - name: University College London, UK
   index: 5
date:  2023
bibliography: paper.bib
---

# Summary

The *profet* (**pro**tein structure **fet**cher) python libary provides a simple and streamlined interface that makes it easy to download protein structures from various online databases. Since its founding in 1971, over 1 million experimentally determined macromolecular structures have been deposited and made freely available to all in the Protein Data Bank (PDB) archive [@pdb]. The availability of this wealth of experimental data has been pivotal in the development of new software in the field. Recently, the AlphaFold2 [@alphafold] team released over 200 million predicted macromolecular structures on their online platform. Being able to easily access these incredible open repositories of experimental and simulated data is crucial for accelerating scientific software development in structural biology. However, in practice, doing this can be cumbersome, as each database has their own manual download system, or individual python package. 

With *profet*, users can conveniently download individual structures directly using python by simply specifying their Uniprot ID [@uniprot]. Users can specify which database they would like to use by default and if the structure is available from that source it will be downloaded. If the structure is not available from that source, *profet* will seek to download it from an alternative database. Typical applications that require the ability to download many structures on demand are protein matching algorithms for visual proteomics, such as [@cryolo] [@affinity], large scale models in molecular dynamics simulations [@mcguffee] [@bigsim], and electron microscopy simulations [@parakeet].


# Statement of need

While there are existing methods available to access and download files from the PDB using python (for example, with the pypdb library [@pypdb]) or R (for example with bio3d library [@bio3d]), AlphaFold and other online databases require users to either manually download files through a web browser or submit raw FTP requests to be able to download files in an automated fashion. Furthermore, currently, each user needs to check whether the structures of interest are available in each database as there is currently no unified method to search through both the PDB and AlphaFold databases simultaneously. The *profet* library provides a convenient unified interface to retrieve structures of biological macromolecules from either the PDB or AlphaFold database, simply by specifying the Uniprot ID.

At the time of writing, the authors are not aware of any other tool that allows a user to download protein structures from multiple databases in a unified interface. Commonly, structures are downloaded directly from the respective portal interfaces. Furthermore, for batch downloads, it is necessary to have scripting skills [@batch]. With computational power increasing and simulation sizes reaching hundreds-of-millions of atoms [@singharoy], it is becoming increasingly important to automate the pipeline of PDB structure access, which *profet* provides a portal to. Furthermore, *profet* is scalable and has the ability to add other databases as search options (such as CATHdb[@cathdb]) by providing a template for accessing database APIs.


# *profet* workflow example
 
The *profet* library has a high-level python API that can be used to download entries from both the PDB and alphafold through a single unified object oriented interface. An example of how to access this functionality through the main protein fetcher class, `profet.Fetcher`, is shown in the following code snippet.

```python=
from profet import Fetcher

# Initialise the fetcher
fetcher = Fetcher("pdb")

# Get the filename and filedata
filename, filedata = fetcher.get_file("4v1w", filetype="cif", filesave=True)

# Print the filename and first few lines of the file
print("Filename for 4v1w = %s" % filename)
print("File contents:")
print(filedata[0:207].decode("ascii"))

# Get the search history
history_dictionary = fetcher.search_history()
```

This results in the following output:

```bash
Filename for 4v1w = 4v1w.cif
File contents:
data_4V1W
# 
_entry.id   4V1W 
# 
_audit_conform.dict_name       mmcif_pdbx.dic 
_audit_conform.dict_version    5.283 
_audit_conform.dict_location   http://mmcif.pdb.org/dictionaries/ascii/mmcif_pdbx.dic 
#
```

During initialisation, the default database can be specified in the constructor of the `profet.Fetcher` class. This should be a string containing either "pdb" for the PDB database or "alphafold" for the AlphaFold database. In the example, the PDB database was specified. After initialisation, the fetcher can then be used to download structures from the specified database. This can be done by using the `profet.Fetcher.get_file` method and by specifiying the `uniprot_id` of the protein of interest. In the example, an apoferritin model ("4v1w") is downloaded. If the entry does not exist, then an exception is raised.

When downloading the protein structure, the `filetype` keyword can also be specified to choose between "cif" or "pdb" file if available. If the requested file type is not available then *profet* will attempt to download whichever file type is available. For example, if "cif" is requested but only "pdb" is available, the pdb file will be downloaded. If no file type is specified then the pdb file will be download if present, otherwise the cif file will be downloaded. Additionally, the `filesave` boolean flag can be used to specify whether or not the protein structure should be saved automatically to disk. By default this is set to False, in which case the returned filename is `None` and only the filedata is returned as a binary string. If `filesave` is `True`, then the file is saved into the current working directory. 

Finally, the `profet.Fetcher.search_history` function can be used to access the list of previously searched structures. The command will show a dictionary of the IDs searched by the fetcher and the databases where they are available. 

```
{'7U6Q': ['pdb'], 'F4HvG8': ['alphafold'], 'A0A023FDY8': ['pdb', 'alphafold']}
```

The functionality can be tested using the `run_profet.ipynb` Jupyter notebook, available in the package repository.

# References 