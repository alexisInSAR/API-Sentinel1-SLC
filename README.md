# API-Sentinel1-SLC

**Set of scripts to download Sentinel-1 data (SLCs and POD orbit files) from the ASF mirror.**

***

# For the SLCs

**To download all the available SLCs:**
- -u (or --username): your id account for ASF mirror
- -p (or --password): your password for ASF mirror
- -s (or --path_SLC): the path for the SLC images
- -r (or --path_RSLC): the path for the coregistred SLC images (only available for GAMMA stacks)
- -b (or --bbox): coordinates for AOI 
- -i (or --date_start): the first date YYYY-MM-DDTHH:mm:SS
- -j (or --date_end): the last date YYYY-MM-DDTHH:mm:SS
- -o (or --orbit_relative): the relative orbit (1 to 999)
- -f (or --flight_direction): the flight direction (a or d, for ascending or descending)
- -m (or --mode): csv to create the list, kml to download a kml file of SLCs
- -w (or --write): y (yes) or n (no) to download the SLC .zip files

```bash
API_download_S1_SLC.py -u username -p password -s . -r . -b -10.78,51.27,-5.03,55.70 -i 2017-01-01T00:00:00 -j 2023-12-31T00:00 -o 1 -f a -m csv -w n
```

***

# For the orbits

**To download the S1 orbits according to the files from the previous script:**
- -f (or --file): .csv list of SLCs (from API_download_S1_SLC.py)
- -o (or --output): the path for the orbits
- -u (or --username): your id account for ASF mirror
- -p (or --password): your password for ASF mirror

```bash
API_orbits_S1.py -f SLC.list -o Orbits -u username -p password
```

***

# Author

The author is:
  - Alexis Hrysiewicz (UCD / iCRAG)
