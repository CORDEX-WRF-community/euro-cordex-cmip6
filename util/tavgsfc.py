#!/usr/bin/env python
#
# tavgsfc.py
#
# Inserts running mean lowest model level temperatures into WRF met_em
# files. The new variable TAVGSFC is used by WRF as skin temperature
# for lakes

import argparse
import glob
import netCDF4 as nc
import numpy as np
import os
import sys

varname ='TAVGSFC'
running_mean_days = 15
files_per_day = 4

def process_wrf_files(pattern, overwrite):
  files = glob.glob(pattern)
  files.sort()
  
  print(f'Inserting {running_mean_days}-day running mean into {varname}')
  running_mean_buffer = []
  for file_name in files:
    print(file_name)
    input_file = nc.Dataset(file_name, 'a')
    tt = input_file.variables['TT'][:]
    if len(running_mean_buffer) == running_mean_days * files_per_day:
      # Remove the oldest time worth of data
      running_mean_buffer.pop(0)
    running_mean_buffer.append(tt[:, 0, :, :])
    running_mean = np.mean(running_mean_buffer, axis=0)
    if varname in input_file.variables:
      print(f'WARNING: Variable {varname} already exists in {file_name}.')
      if overwrite:
        print('Overwriting...')
        input_file.variables[varname][:] = running_mean
      else:
        print('Skipping...')
        input_file.close()
        continue
    else:
      # close the input file as it will be modified
      input_file.close()
      # extract SST into dummy file (this is to be replaced by the running mean of TT)
      os.system("ncks -v SST "+file_name+" dummy.nc") 
      # rename SST in dummy file to TAVGSFC
      os.system("ncrename -h -O -v SST,"+varname+" dummy.nc") 
      # append TAVGSFC back to the original input file
      os.system("ncks -A -C -v "+varname+" dummy.nc "+file_name) 
      # remove the dummy file
      os.system("rm dummy.nc") 
      # reopen the input file (TAVGSFC was added)
      input_file = nc.Dataset(file_name, 'a') 
      # replace TAVGSFC with running mean
      input_file.variables[varname][:] = running_mean 
      # set the description attribute (now all attributes are correct)
      setattr(input_file.variables[varname], 'description', '2 m Temperature') # 
    # Add the global attribute flag
    input_file.setncattr('FLAG_TAVGSFC', 1)
    input_file.close()
  

def main():
  parser = argparse.ArgumentParser(
    description='Process WRF met_em files and add running mean temperature'
  )
  parser.add_argument('pattern',
    help='File pattern to match met_em files'
  )
  parser.add_argument('-O', '--overwrite', action='store_true',
    help='Overwrite TAVGSFC if it already exists'
  )
  args = parser.parse_args()
  process_wrf_files(args.pattern, args.overwrite)

if __name__ == "__main__":
    main()
