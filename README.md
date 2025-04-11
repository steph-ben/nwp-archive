# Simple scripts to download NWP Archive

## Getting started

* Get the script
```shell
$ git clone git@github.com:steph-ben/nwp-archive.git
$ pip
```

* Requirements 
```shell
$ python -V
Python 3.13.2
$ wgrib2 --version
v3.1.3 10/2023  Wesley Ebisuzaki, Reinoud Bokhorst, John Howard, Jaakko Hyvätti, Dusan Jovic, Daniel Lee, Kristian Nilssen, Karl Pfeiffer, Pablo Romero, Manfred Schwarb, Gregor Schee, Arlindo da Silva, Niklas Sondell, Sam Trahan, George Trojan, Sergey Varlamov
```



## GFS usage

* Check domain / steps / parameters configuration


```shell
$ more get_gfs.py
...
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
...
```

* Launch script

```shell
$ python get_gfs.py 2022

# Temporary directory with files with full data
$ tree -h gfs_data/
[   26]  gfs_data/
└── [   16]  gfs.20220101
    └── [   19]  00
        └── [   38]  atmos
            └── [ 342M]  gfs.t00z.pgrb2.0p25.f030

# Directory with files with subset data
$ tree -h subset_data/
[   26]  subset_data/
└── [   16]  gfs.20220101
    └── [   19]  00
        └── [ 4.0K]  atmos
            ├── [ 103K]  subset_gfs.t00z.pgrb2.0p25.f000
            ├── [ 103K]  subset_gfs.t00z.pgrb2.0p25.f003
            ├── [ 103K]  subset_gfs.t00z.pgrb2.0p25.f006
            ├── [ 103K]  subset_gfs.t00z.pgrb2.0p25.f009
            ├── [ 103K]  subset_gfs.t00z.pgrb2.0p25.f012

```
