# CORDEX-CMIP6 simulations with WRF for EURO-CORDEX

This is the base repository for the CORDEX-CMIP6 coordinated WRF runs started in 2021. 

It may contain, also in different git branches, everything (=namelists, TBL, files, cookbooks, documentation etc.) to create static fields and forcing data and to run WRF for the CORDEX-CMIP6 evaluation, historical, and projection runs according go the CORDEX-CMIP6 protocol as of 2021. The master branch should always contain the most recent community-agreed configuration.

Some usage idea for the repository: When testing different configurations during the evaluation runs, different branches can be used and later on merged with the master. Also, when individual groups start populating the repository with their specific files, they should be out in a separate branch rather than into the master. Preprocessing scripts and configurations for different GCMs could be kept in separate subdirectories.
Please, keep this **repository free from large binary files**. Just link them from a remote URL.

The WRF version agreed to be used for these simulations is V4.4.2. There are several bugs in NoahMP that affect this version, so it is recommended to use directly the branch v4.4.2-EUR from the CORDEX WRF community fork:
```bash
git clone --recurse-submodules -b v4.4.2-EUR  https://github.com/CORDEX-WRF-community/WRF.git
```

For reference, you can check here the modifications introduced to the NoahMP code (most come from the official release):

https://github.com/CORDEX-WRF-community/noahmp/compare/v4.4.2..v4.4.2-EUR
