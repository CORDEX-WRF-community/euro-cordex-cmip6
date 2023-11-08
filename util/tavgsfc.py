#!/usr/bin/env python
#
# tavgsfc.py v0.2 (2023-11-08)
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
      tavgsfc = input_file.createVariable(varname, 'f4', ('Time', 'south_north', 'west_east'))
      for attr_name in input_file.variables['TT'].ncattrs():
        setattr(tavgsfc, attr_name, getattr(input_file.variables['TT'], attr_name))
      setattr(tavgsfc, 'MemoryOrder', 'XY ')
      tavgsfc[:] = running_mean
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
