"""
Help do the following :
- Download GFS archive from AWS https://noaa-gfs-bdp-pds.s3.amazonaws.com/
- Locally subset domain
- Locally subset parameters
"""
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import argparse
from concurrent.futures import ThreadPoolExecutor

# ========== CONFIGURATION ==========
cycles = ["00", "06", "12", "18"]  # Multiple forecast cycles per day
forecast_hours = list(range(0, 387, 3))
param_matches = [
    ":TMP:2 m above ground:",
    ":UGRD:10 m above ground:",
    ":VGRD:10 m above ground:"
]

# Geographic subset
lon_min, lon_max = 230, 300
lat_min, lat_max = 30, 50
# ========== CONFIGURATION ==========

output_dir = Path("gfs_data")
output_dir.mkdir(parents=True, exist_ok=True)


def process_file(date: datetime, cycle: str, fhr: int):
    date_str = date.strftime("%Y%m%d")
    fhr_str = f"{fhr:03d}"
    gfs_subdir = f"gfs.{date_str}/{cycle}/atmos"
    filename = f"gfs.t{cycle}z.pgrb2.0p25.f{fhr_str}"

    # Paths
    local_dir = output_dir / gfs_subdir
    subset_dir = Path("subset_data") / gfs_subdir
    local_dir.mkdir(parents=True, exist_ok=True)
    subset_dir.mkdir(parents=True, exist_ok=True)

    local_file = local_dir / filename
    subset_file = subset_dir / f"subset_{filename}"

    # Check if download is needed
    if not subset_file.exists() and not local_file.exists():
        url = f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/{gfs_subdir}/{filename}"
        curl_cmd = ["curl", "-f", "-o", str(local_file), url]
        print(f"⬇️  Running curl: {' '.join(curl_cmd)}")

        result = subprocess.run(curl_cmd)
        if result.returncode != 0 or not local_file.exists():
            print(f"❌ Download failed: {url}")
            return
        print(f"✅ File downloaded : {local_file.absolute()}")

    if not subset_file.exists():
        print(f"📦 Subsetting {filename} | Cycle: {cycle} | Var: {param_matches}")
        wgrib2_cmd = [
            "wgrib2", str(local_file),
            "-match", #f"'{param_match}'",
            "|".join(param_matches),
            "-small_grib",  f"{lon_min}:{lon_max}", f"{lat_min}:{lat_max}",
            str(subset_file)
        ]
        print(" ".join(wgrib2_cmd))
        result = subprocess.run(wgrib2_cmd)

        if result.returncode == 0:
            print(f"✅ Saved subset: {subset_file}")
        else:
            print(f"❌ Subset failed: {subset_file}")

        if subset_file.exists() and subset_file.stat().st_size > 0:
            local_file.unlink()


def run_for_year(year: int, max_workers: int = 4):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    jobs = []

    current_date = start_date
    while current_date < end_date:
        for cycle in cycles:
            for fhr in forecast_hours:
                jobs.append((current_date, cycle, fhr))
        current_date += timedelta(days=1)

    print(f"🌀 Running {len(jobs)} jobs with {max_workers} threads...")
    #with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #    executor.map(lambda args: process_file(*args), jobs)
    for job in jobs:
        process_file(*job)


# ========== MAIN ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download & subset GFS data by year with multiple cycles and variables.")
    parser.add_argument("year", type=int, help="Year to process (e.g., 2021)")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel threads")
    args = parser.parse_args()

    run_for_year(args.year, args.workers)
