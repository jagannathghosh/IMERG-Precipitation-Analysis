# IMERG-Precipitation-Analysis
This project processes IMERG satellite precipitation data (NetCDF) to generate daily accumulated rainfall and time series analysis over the Indian Summer Monsoon (ISM) period.

## Features
- Convert NetCDF time to readable date format
- Extract precipitation data (precipitationCal)
- Aggregate 8 time steps (00Z–21Z) into daily rainfall
- Handle missing values (-9999.9 → 0)
- Generate daily precipitation matrices
- Save processed data into .mat files
- Compute spatial mean precipitation
- Plot daily precipitation time series

## Data
- IMERG precipitation data (.nc)
- Time period: JJAS (June–September)
- Years: 2000–2024

Note: Data is not included due to large file size

## Project Structure
imerg-precipitation-analysis/
│── imerg_analysis.py
│── README.md
│── requirements.txt


## Requirements
Install dependencies:
pip install -r requirements.txt

## How to Run
1. Update data path in script:
folder = "data/IMERG/"

2. Run:
python imerg_analysis.py

## Output
- Daily precipitation matrices
- .mat files
- Time series plots

## Applications
- Monsoon rainfall analysis
- Climate studies
- Hydrology and flood analysis

## Author
Jagannath Ghosh  
IISER Berhampur
