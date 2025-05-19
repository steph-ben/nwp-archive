from pathlib import Path

from ecmwfapi import ECMWFService
from datetime import datetime, timedelta

"""
Selected run : 00h and 12h (only those available) - we need both
Forecast steps : from 00h to 360h (all available) - we need from 00h to 132h
Domain : we need the following region:
lon_min, lon_max = 30.76, 63.97
lat_min, lat_max = 11.03, 40.88

Selected surface parameters: 
Grib codes : 165.128/166.128/167.128/207.128/260242
temperature 2m
relative humidity 2m
wind speed and wind direction 10m
accumulated precippitation

Selected pressure level parameters : 
Levels : 850 / 700 / 500 hpa
Grib codes : 129.128/130.128/131/132/157.128
temperature
relative humidity
wind speed and direction
geopotential height
All the parameters you have listed are correct
Format : GRIB
Output file : Depending on ECMWF requests, we might have one file per run or per day - we prefer one file per run
"""
server = ECMWFService("mars")

def daterange(start_date, end_date):
    """Generate date range with valid days"""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

# === USER CONFIGURATION ===
start_year = 2024
end_year = 2024
runs = ["00", "12"]
steps = '/'.join(map(str, range(0, 135, 6)))  # 0h to 132h every 6h
area = '41/31/12/64'  # N/W/S/E
grid = '0.1/0.1'
time_ = "00:00:00/12:00:00"
date_ = "2024-01-01/to/2024-01-31"

params_sfc = "165.128/166.128/167.128/207.128/260242"
params_sfc = "165.128/166.128/167.128/168.128" #/228.128"
params_pl = "129.128/130.128/131/132/157.128"
levels_pl = "500/700/850"


# server.execute({
#     'class': 'od',
#     'stream': 'oper',
#     'expver': '1',
#     'type': 'fc',
#     'date': "2025-01-01",
#     'levtype': 'sfc',
#     'param': params_sfc,
#     'time': "00:00:00",
#     'step': steps,
#     'area': area,
#     'grid': '0.1/0.1',
#     # 'format': 'grib2',
#     },
#     "test_area_g.grib"
# )
# exit()

# === DATE RANGE ===
start_date = datetime(start_year, 1, 1)
end_date = datetime(end_year, 12, 31)

# === MAIN DOWNLOAD LOOP ===
for single_date in daterange(start_date, end_date):
    date_str = single_date.strftime('%Y-%m-%d')
    yyyymmdd = single_date.strftime('%Y%m%d')
    dest = Path(f'/mnt/data_samples/Koweit/IFS_Archive/{single_date:%Y/%m/%d}')
    dest.mkdir(parents=True, exist_ok=True)

    for run in runs:
        print(f"Requesting {date_str} run {run}...")

        fp_sfc = Path(f'{dest}/ecmwf_{yyyymmdd}_{run}z_sfc.grib')
        if not fp_sfc.exists():
            server.execute({
                'class': 'od',
                'stream': 'oper',
                'expver': '1',
                'type': 'fc',
                'date': date_str,
                'levtype': 'sfc',
                'param': params_sfc,
                'time': run,
                'step': steps,
                'area': area,
                'grid': grid,
                'format': 'grib2',
                },
                fp_sfc
            )

        fp_pl = Path(f'{dest}/ecmwf_{yyyymmdd}_{run}z_pl.grib')
        if not fp_pl.exists():
            server.execute({
                'class': 'od',
                'stream': 'oper',
                'expver': '1',
                'type': 'fc',
                'date': date_str,
                'levtype': 'pl',
                'level': levels_pl,
                'param': params_pl,
                'time': run,
                'step': steps,
                'area': area,
                'grid': grid,
                'format': 'grib2',
                },
                fp_pl
            )

#
# # === DATE RANGE ===
# start_date = datetime(start_year, 1, 1)
# end_date = datetime(end_year, 12, 31)
#
# # === MAIN DOWNLOAD LOOP ===
# for single_date in daterange(start_date, end_date):
#     date_str = single_date.strftime('%Y-%m-%d')
#     yyyymmdd = single_date.strftime('%Y%m%d')
#     for run in runs:
#         print(f"Requesting {date_str} run {run}...")
#
#         # Surface-level request
#         server.retrieve({
#             'dataset': 'tigge',
#             'class': 'od',
#             'stream': 'oper',
#             'type': 'fc',
#             'expver': '1',
#             'date': date_str,
#             'time': run,
#             'step': steps,
#             'levtype': 'sfc',
#             'param': '165.128/166.128/167.128/207.128/260242',
#             'area': area,
#             'grid': grid,
#             'format': 'grib2',
#             'target': f'ecmwf_fc_sfc_{yyyymmdd}_{run}z.grib',
#         })
#
#         # Pressure-level request
#         server.retrieve({
#             'dataset': 'tigge',
#             'class': 'od',
#             'stream': 'oper',
#             'type': 'fc',
#             'expver': '1',
#             'date': date_str,
#             'time': run,
#             'step': steps,
#             'levtype': 'pl',
#             'levelist': '850/700/500',
#             'param': '129.128/130.128/131/132/157.128',
#             'area': area,
#             'grid': grid,
#             'format': 'grib2',
#             'target': f'ecmwf_fc_pl_{yyyymmdd}_{run}z.grib',
#         })
