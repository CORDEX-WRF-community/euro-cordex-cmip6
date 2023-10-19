# CORDEX-CMIP6 simulations with WRF for EURO-CORDEX

This is the base repository for the CORDEX-CMIP6 coordinated WRF runs started in 2021. 

It may contain, also in different git branches, everything (=namelists, TBL, files, cookbooks, documentation etc.) to create static fields and forcing data and to run WRF for the CORDEX-CMIP6 evaluation, historical, and projection runs according to the [CORDEX-CMIP6 protocol](https://cordex.org/wp-content/uploads/2021/05/CORDEX-CMIP6_exp_design_RCM.pdf).
The `main` branch should always contain the most recent community-agreed configuration.
Please, keep this **repository free from large binary files**. Just link them from a remote URL.

## Resources

The WRF version agreed to be used for these simulations is V4.5.1. There are several bugs in NoahMP that were fixed in this version, but some remain, so it is recommended to use directly the branch v4.5.1-EUR from the _CORDEX WRF community_ fork:
```bash
git clone --recurse-submodules -b v4.5.1.2  https://github.com/CORDEX-WRF-community/WRF.git
```
The configuration for the default EURO-CORDEX CMIP6 runs requires also:

|File | Description |
|-----|-------------|
| [namelist.input](./namelist.input) | WRF namelist file in this repository. |
| [geo_em.d01.nc](https://meteo.unican.es/work/josipa/euro-cordex-cmip6/static_data/geo_em.d01_EUR-11_newLAI_LANDMATE_final.nc) | Static data on the EUR-11 rotated lon-lat grid. See [static_data](./static_data) folder for details.|
