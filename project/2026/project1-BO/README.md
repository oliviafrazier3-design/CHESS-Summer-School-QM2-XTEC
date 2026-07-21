
# **File structure of QM2 Beamline data**


The output file structure from nxrefine should look something like the following:
- Datafile: `/nfs/chess/id4b/2025-2/sarker-0000-a/raw6m/sample_name/sample_id/temp/sample_name_scannumber/sample_name_PIL10_009_00001.cbf`
```
nfs
└── chess
    └── id4b
        └── 2025-2
            └── chess
                └── sarker-0000-a
                        └── raw6m
                            └── sample_name
                                └── sample_id
                                  └── 14
                                      └── sample_name_scannumber
                                            └── sample_name_PIL10_009_00001.cbf
                                            └── sample_name_PIL10_009_00002.cbf
                                            └── sample_name_PIL10_009_00001.cbf
                                            └── ...
          
                                  ├── 300
                                      └── sample_name_scannumber
                                            └── sample_name_PIL10_009_00001.cbf
                                            └── sample_name_PIL10_009_00002.cbf
                                            └── sample_name_PIL10_009_00001.cbf
                                            └── ...
```

The file that we are interested in loading is the .cbf file with the form `sample_name_PIL10_009_00001.cbf`, which holds information
