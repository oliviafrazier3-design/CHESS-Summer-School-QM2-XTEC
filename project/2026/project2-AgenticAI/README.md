# **File structure of QM2 Beamline data**


The output file structure from nxrefine should look something like the following:
- Datafile: `/nfs/chess/id4baux/2025-2/sarker-0000-a/nxrefine/sample_name/sample_id/RbV3Sb5_14.nxs`
```
nfs
└── chess
    └── id4baux
        └── 2025-2
            └── chess
                └── sarker-0000-a
                        └── nxrefine
                            └── sample_name
                                └── sample_id
                                    └── filename_14
                                                ├── 14
                                                |    └── transform.nxs
        
                                                ├── 300
                                                |    └── transform.nxs
                                                ├── filename_15.nxs
                                                ├── filename_100.nxs
                                                └── filename_300.nxs
```

The file that we are interested in loading is the .nxs file with the form `filename_14.nxs`, which holds information about the scan at _T_ = 14 K. This file has a `NXlink` which references an external file with the intensity values, stored in `15/transform.nxs`. In other words, `filename_14.nxs` contains sample metadata such as the orientation matrix, temperature, ion chamber counts, etc. and the file `transform.nxs` is simply an array-like container for the pixels that make up the oriented HKLI data.

Usually, we are not interested in the metadata, but if you are interested in accessing the scan metadata, we can use the `nexusformat` package, specifically the `nexusformat.nexus.nxload()` function to open the file. Otherwise, here we provide functions that allow you to directly load the HKLI data without the extra metadata.
