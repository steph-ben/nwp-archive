from ecmwfapi import ECMWFDataServer
from datetime import datetime, timedelta

server = ECMWFDataServer()

def daterange(start_date, end_date):
    """Generate date range with valid days"""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

# === USER CONFIGURATION ===
start_year = 2015
end_year = 2020
runs = ["00", "12"]
steps = '/'.join(map(str, range(0, 135, 6)))  # 0h to 132h every 6h
area = '40.88/30.76/11.03/63.97'  # N/W/S/E
grid = '0.25/0.25'  # Optional: ECMWF native is 0.1

# === DATE RANGE ===
start_date = datetime(start_year, 1, 1)
end_date = datetime(end_year, 12, 31)

# === MAIN DOWNLOAD LOOP ===
for single_date in daterange(start_date, end_date):
    date_str = single_date.strftime('%Y-%m-%d')
    yyyymmdd = single_date.strftime('%Y%m%d')
    for run in runs:
        print(f"Requesting {date_str} run {run}...")

        # Surface-level request
        server.retrieve({
            'dataset': 'tigge',
            'class': 'od',
            'stream': 'oper',
            'type': 'fc',
            'expver': '1',
            'date': date_str,
            'time': run,
            'step': steps,
            'levtype': 'sfc',
            'param': '165.128/166.128/167.128/207.128/260242',
            'area': area,
            'grid': grid,
            'format': 'grib2',
            'target': f'ecmwf_fc_sfc_{yyyymmdd}_{run}z.grib',
        })

        # Pressure-level request
        server.retrieve({
            'dataset': 'tigge',
            'class': 'od',
            'stream': 'oper',
            'type': 'fc',
            'expver': '1',
            'date': date_str,
            'time': run,
            'step': steps,
            'levtype': 'pl',
            'levelist': '850/700/500',
            'param': '129.128/130.128/131/132/157.128',
            'area': area,
            'grid': grid,
            'format': 'grib2',
            'target': f'ecmwf_fc_pl_{yyyymmdd}_{run}z.grib',
        })
