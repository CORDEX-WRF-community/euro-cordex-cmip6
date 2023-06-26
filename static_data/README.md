# Static data in WRF-CORDEX-EUR-11 simulations

This folder provides access to the final geogrid file [geo_em.d01_EUR-11_newLAI_LANDMATE_final.nc](https://meteo.unican.es/work/josipa/euro-cordex-cmip6/static_data/geo_em.d01_EUR-11_newLAI_LANDMATE_final.nc) in which default static data at highest available resolution have been used for most variables.
These default static data have been downloaded from [wrf user page](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html).
The file also containis variables based on 3 new data sets that have been adapted for WPS:

1. **Leaf area index (LAI)** data are based on SPOT satellite data downloaded from [CDS](https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-lai-fapar?tab=overview) and processed for use in WPS. Data are monthly mean values over period of 15 years  (i.e. from 1999 to 2014) at 30s resolution.
The decision to use these new data set in the new EURO-CORDEX runs was taken in November 2022.
This was based on the test run performed by AUTH and the analysis in [LAI_analysis_map_vs_table.pdf](https://meteo.unican.es/work/josipa/euro-cordex-cmip6/static_data/LAI_analysis_map_vs_table.pdf).
NOTE: In winter months, due to the position of the SPOT satellite, missing values appear in the far north of the EUR-11 CORDEX domain. These values are filled with the values from the default LAI map based on MODIS LAI data, also avilable at 30s resolution.
All the details on the preprocessing procedure can be found in the github repository [lai4wrf](https://github.com/AEI-CORDyS/lai4wrf).
Contact person: Josipa Milovac 

2. **Land use data** is based on [LANDMATE PFT](https://www.wdc-climate.de/ui/entry?acronym=LM_PFT_EUR_v1.1) land cover dataset for Europe 2015, the most recent version v1.1. The file [New_PFTs_v2.docx.pdf](./New_PFTs_v2.docx.pdf) provides a description on the methodoloy applied for the preparation of the map for the WRF geo_em file. Contact person: Rita M. Cardoso 

3. **Top soil texture data** are based on the global Harmonized World Soil Database v 1.2 at 30s resolution [HWSD](https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v12/en/) and Soil Map of Germany 1:1 000 000 [BÜK1000](https://www.bgr.bund.de/DE/Themen/Boden/Informationsgrundlagen/Bodenkundliche_Karten_Datenbanken/BUEK1000/buek1000_node.html) over Germany. These data sets are both adapted for WRF and published ([Milovac et al. 2018](doi:10.1594/WDCC/WRF_NOAH_HWSD_world_TOP_ST_v121); [Milovac et al., 2014](doi:10.1594/WDCC/WRF_NOAH_BUK_Ger_top_SOILTYP)).

Filling the missing data gaps of LAI data and fixing the category for the Black Sea was done using [notebook](./update_static_data.ipynb). All the intemediate geogrid files can be downloaded from the links given in the same notebook, and for the final geogrid file also here is the download [link](https://meteo.unican.es/work/WRF4CORDEX_geogrid_files/geo_em.d01_EUR-11_new_BlackSea2sea.nc).
Contact person: Josipa Milovac 

We also provide an additional geogrid file ([geo_em.d01_EUR-11_newLAI_CORINE.nc](https://meteo.unican.es/work/josipa/euro-cordex-cmip6/static_data/geo_em.d01_EUR-11_newLAI_CORINE.nc)) that contains the land use data based on [CORINE data](https://land.copernicus.eu/pan-europe/corine-land-cover) (COoRdination of INformation on the Environment), which is on 100m horizontal resolution and more up-to-date than the default MODIS data set. Raw CORINE defines more land use classes than the MODIS data set available for WPS, therefore the preparation included (1) re-classification to the MODIS land cover categories to allow a straightforward implementation into WPS, (2) merging the appropriate categories within a Geographic Information System (GIS) software, and (3) the conversion to WPS readable data with [`convert_geotiff`](https://github.com/openwfm/convert_geotiff)’ utility ([Bauer et al., 2020](https://a.tellusjournals.se/article/10.1080/16000870.2020.1761740/)). The data set covers only Europe, and the missing part outside of Europe, which is within the EUR-11 domain, is filled with the default MODIS data at 15s resolution.
Contact person: Hans-Stefan Bauer 
