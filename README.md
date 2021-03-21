# cordex-cmip6_wrf-users_base

This is the base repository for the CORDEX-CMIP6 coordinated WRF runs started in 2021. 

It may contain, also in different git branches, everything (=namelists, TBL, files, cookbooks, documentation etc.) to create static fields and forcing data and to run WRF for the CORDEX-CMIP6 evaluation, historical, and projeciton runs according go the CORDEX-CMIP6 protocol as of 2021. The "master branch" should always contain the most recent community-agreed configuration.

Some usage idea for the repository: When testing different configurations during the evaluation runs, different branches can be used and later on merged with the master. Also, when individual groups start populating the repository with their specific files, they should be out in a separate branch rather than into the master. Preprocessing scripts and configurations for different GCMs could be kept in separate subdirectories.

When CORDEX-CMIP6 further differentiates itself into more subprojects then more repositories might be created within the gitlab subgroup "cordex-cmip6". 

For more information, until this README.md file of the base repository for the CORDEX-CMIP6 WRF runs has been properly updated, see the README.md file of the FPSCONV D-experiments as part of this private gitlab CORDEX group: https://gitlab.com/cordex/cordex-fpsconv/cordex-fpsconv_wrf-users_exp-d/-/blob/master/README.md

See also here for additional details: https://docs.google.com/document/d/1w85cyVFK_p88ReN1lLeng0b2bqyI62K4Hb8sE5bSqlU
