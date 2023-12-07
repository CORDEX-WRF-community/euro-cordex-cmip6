# Functionality of the script:
# (1) checks if there is a restart file in the WRF/run folder, an if so reads the start date.
#      If not, the start date will be read from the namelist.input. 
# (2) sets the right start and end date in the namelist.input (end date is set to be the start date + 1year)  
# (3) extracts the correct dates from multiple aerosol files that need to be placed in the WRF/run folder 
# (4) creates the file named "AOD_{DOMAIN}" 
# (5) updates CO2 in MPTABLE.TBL accorinig to the starting year
# 
# To run the script: python update_and_restart.py

import re
import os
import sys
import netCDF4 as nc
import numpy as np
import subprocess
import glob
import calendar
from datetime import datetime, timedelta

# Constants
DOMAIN = 'd01'
FOLDER_PATH = './'
PATTERN = f'wrfrst_{DOMAIN}'
NAMELIST = 'namelist.input'
#
# Functions
#
def extract_date_from_filename(filename, pattern):
    match = re.search(pattern, filename)
    return match.group(1) if match else None

def day_in_year(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").timetuple().tm_yday

def ndays_per_year(year):
    return 366 if calendar.isleap(year) else 365

def read_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_lines_to_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)
        
def is_netcdf_file_complete(file_path):
    try:
        with nc.Dataset(file_path, 'r') as ncfile:
            # If the file can be opened without errors, it's considered complete
            return True
    except FileNotFoundError:
        print(f"The NetCDF file '{file_path}' does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred while opening the file '{file_path}': {e}")
        return False
#
# Extract start date from the latest restart files or from the namelist.input
#
nc_files = [file for file in os.listdir(FOLDER_PATH) if file.startswith(PATTERN)]

if nc_files:
    print(f"Reading start date from the restart file.")
    nc_files.sort(key=lambda x: os.path.getctime(os.path.join(FOLDER_PATH, x)), reverse=True)
    latest_nc_files = nc_files[:2]
    dates = [extract_date_from_filename(file, r"(\d{4}-\d{2}-\d{2})") for file in latest_nc_files]
    if is_netcdf_file_complete(latest_nc_files[0]):
        date=dates[0]
    elif len(latest_nc_files) < 2:
        print(f'Restart date cannot be extracted from a restart file, the file is not complete. Exiting...')
        sys.exit()
    else:
        date=dates[1]
    restart_date = datetime.strptime(date, "%Y-%m-%d")
    print(f"Restart date is: {restart_date.strftime('%Y-%m-%d')}")
    
    # Update restart dates in the namelist
    lines = read_lines_from_file(NAMELIST)
    for i, line in enumerate(lines):
        if "start_year" in line:
            lines[i] = f" start_year                          = {restart_date.year}, {restart_date.year},\n"
        elif "start_month" in line:
            lines[i] = f" start_month                         = {restart_date.month:02d}, {restart_date.month:02d},\n"
        elif "start_day" in line:
            lines[i] = f" start_day                           = {restart_date.day:02d}, {restart_date.day:02d}\n"
        elif "end_year" in line:
            lines[i] = f" end_year                            = {restart_date.year+1}, {restart_date.year+1}\n"
        elif "end_month" in line:
            lines[i] = f" end_month                           = {restart_date.month:02d}, {restart_date.month:02d}\n"
        elif "end_day" in line:
            lines[i] = f" end_day                             = {restart_date.day:02d}, {restart_date.day:02d}\n"

    write_lines_to_file(NAMELIST, lines)

else:
    print(f"No valid restart file found. Reading from namelist.")

    # Extract initial date from namelist
    lines = read_lines_from_file(NAMELIST)
    date_format = "%Y-%m-%d"
    for i, line in enumerate(lines):
        if "start_year" in line:
            print(line)
            year = int(line.split('=')[1].split(',')[0].strip())
        elif "start_month" in line:
            month = int(line.split('=')[1].split(',')[0].strip())
        elif "start_day" in line:
            day = int(line.split('=')[1].split(',')[0].strip())
    
    restart_date = datetime(year, month, day)
    print(f'Initial date read from namelist.input is: {restart_date.strftime("%Y-%m-%d")}')
    
#
# Extract correct AOD files from the complete list of yearly AOD files in WRF/run directory
#
output_file = f'AOD_{DOMAIN}'
start_time = restart_date.strftime('%Y-%m-%d')
end_time = (restart_date + timedelta(days=ndays_per_year(restart_date.year))).strftime('%Y-%m-%d')
start_timestep = day_in_year(start_time) - 1
last_timestep = day_in_year(end_time) + ndays_per_year(restart_date.year) - 1

file1 = glob.glob(os.path.join('./', f'AOD*_{restart_date.year}*{DOMAIN}*'))
file2 = glob.glob(os.path.join('./', f'AOD*_{restart_date.year+1}*{DOMAIN}*'))

if os.path.exists(output_file):
    os.remove(output_file)

if os.path.exists(f'merged_{DOMAIN}.nc'):
    os.remove(f'merged_{DOMAIN}.nc')

if file1:
    if file1 and file2:
        try:
            subprocess.run([f'ncrcat {file1[0]} {file2[0]} merged_{DOMAIN}.nc'], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f'Command failed with return code {e.returncode}')
            
    elif file1 and not file2:
        subprocess.run([f'cp {file1[0]} merged_{DOMAIN}.nc'], check=True, shell=True)
        last_timestep = ndays_per_year(restart_date.year) - 1

    subprocess.run(['ncks', '-d', 'Time,{},{}'.format(start_timestep, last_timestep), f'merged_{DOMAIN}.nc', output_file], check=True)
    subprocess.run(['rm', f'merged_{DOMAIN}.nc'], check=True)
    print(f'{output_file} from {start_time} until {end_time} successfully created!')

else:
    print(f'AOD files for the year {restart_date.year} are missing. Provide the files and rerun the script!')
#
# Update MPTABLE
#
ghg_file = './CAMtr_volume_mixing_ratio.SSP370'
mptable = './MPTABLE.TBL'
target_string = "!co2 partial pressure"

# Extract target year from namelist.input
with open("./namelist.input", 'r') as file:
    target_year = int(file.read().split('start_year')[1].split('=')[1].split(',')[0])

# Extract CO2 value from ghg_file for the target year
lines = read_lines_from_file(ghg_file)
for line in lines:
    if line.startswith(f'{target_year}'):
        CO2_update = line.split()[1]

# Update MPTABLE with the new CO2 value
lines = read_lines_from_file(mptable)
for i, line in enumerate(lines):
    if target_string in line:
        lines[i] = f'  CO2 = {CO2_update}e-06 !co2 partial pressure \n'
        print(f'Line {i} updated for the year {target_year}, with CO2 = {CO2_update}.')        
write_lines_to_file(mptable,lines)
