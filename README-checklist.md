# Checklist to start running EURO-CORDEX WRF simulations

The steps to run the WRF:

 - [ ] Get your code from CWC WRF v4.5.1.3 \
```git clone --recurse-submodules -b v4.5.1.3  https://github.com/CORDEX-WRF-community/WRF.git```

 - [ ] Adjust the calendar to that of your driving GCM before compiling the code

 - [ ] Place in your running folder all required files:

   - [ ] `iofields.txt` (check if you need additional variables)
   - [ ] link the GHG concentration file corresponding to your driving GCM scenario. E.g. for SSP3-7.0:
     ```bash
     ln -sh CAMtr_volume_mixing_ratio.SSP370 CAMtr_volume_mixing_ratio```
   - [ ] Add the aerosol files corresponding to your driving GCM (e.g. `AOD_d01`) and corresponding to the exact start date of your run (see [#6](https://github.com/CORDEX-WRF-community/euro-cordex-cmip6/issues/6))
   - [ ] Update MPTABLE.TBL to the CO2 concentration of the corresponding year (see [#1](https://github.com/CORDEX-WRF-community/euro-cordex-cmip6/issues/1))
   - [ ] Update your `namelist.input` to match your aerosol file name (e.g. `auxinput15_inname = 'AOD_d01'`)
