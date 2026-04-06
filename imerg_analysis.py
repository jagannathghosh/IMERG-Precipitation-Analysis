##################################Covert Into readable date and time#####################
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from scipy.io import loadmat
import scipy.io as sio
from datetime import timedelta
import xarray as xr
import netCDF4 as nc
from datetime import datetime
import netCDF4 as nc
import numpy as np
folder = r"D:\MS Thesis\ppt_IMERG\IMERG-2000-JJAS-03Z-0.1DD-ISM.nc"
ds = nc.Dataset(folder)
time_var = ds.variables['time'][:]
time_units = ds.variables['time'].units
time_calendar = ds.variables['time'].calendar
readable_time = nc.num2date(time_var, units=time_units, calendar=time_calendar)
date1 = [dt.strftime('%m-%d ') for dt in readable_time]

#################____apply matrix sum_____######################################
files = [
    "IMERG-2024-JJAS-00Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-03Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-06Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-09Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-12Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-15Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-18Z-0.1DD-ISM.nc",
    "IMERG-2024-JJAS-21Z-0.1DD-ISM.nc"
]

folder = r"D:\MS Thesis\ppt_IMERG"
sum_matrix = None

for f in files:
    path = folder + "\\" + f
    ds = nc.Dataset(path)
    time_var = ds.variables['time'][:]
    time_units = ds.variables['time'].units
    time_calendar = ds.variables['time'].calendar
    time_dates = nc.num2date(
        time_var, units=time_units, calendar=time_calendar)
    index = [i for i, t in enumerate(time_dates) if (
        t.year, t.month, t.day) == (2024, 6, 2)]
    if index:
        precip = ds.variables['precipitationCal'][index[0], :, :]
        precip = np.where(precip == -9999.9, 0, precip)
        sum_matrix = precip if sum_matrix is None else sum_matrix + precip
    ds.close()

################_____extract precipitationCal_____##############
file_00z = r"D:\MS Thesis\ppt_IMERG\IMERG-2004-JJAS-00Z-0.1DD-ISM.nc"
file_03z = r"D:\MS Thesis\ppt_IMERG\IMERG-2024-JJAS-03Z-0.1DD-ISM.nc"
ds_00z = xr.open_dataset(file_00z)
ds_03z = xr.open_dataset(file_03z)

precip_00z = ds_00z['precipitationCal']
precip_03z = ds_03z['precipitationCal']

precip_00z_np = precip_00z.values
precip_03z_np = precip_03z.values

####################____maxrix sum for all__#####################
files = ["IMERG-2000-JJAS-00Z-0.1DD-ISM.nc", "IMERG-2000-JJAS-03Z-0.1DD-ISM.nc", "IMERG-2000-JJAS-06Z-0.1DD-ISM.nc", "IMERG-2000-JJAS-09Z-0.1DD-ISM.nc",
         "IMERG-2000-JJAS-12Z-0.1DD-ISM.nc", "IMERG-2000-JJAS-15Z-0.1DD-ISM.nc", "IMERG-2000-JJAS-18Z-0.1DD-ISM.nc", "IMERG-2000-JJAS-21Z-0.1DD-ISM.nc"]
folder = r"D:\MS Thesis\ppt_IMERG"
dates = [datetime(2000, 6, 2) + timedelta(days=i)
         for i in range((datetime(2000, 9, 30) - datetime(2000, 6, 2)).days + 1)]
sample_file = nc.Dataset(folder + "\\" + files[0])
sample_data = sample_file.variables['precipitationCal'][0, :, :]
shape_y, shape_x = sample_data.shape
sample_file.close()

all_ppt_2000nn = np.zeros((len(dates), shape_y, shape_x), dtype=np.float32)

for day_idx, date in enumerate(dates):
    sum_matrix = np.zeros((shape_y, shape_x), dtype=np.float32)
    for f in files:
        path = folder + "\\" + f
        ds = nc.Dataset(path)
        time_var = ds.variables['time'][:]
        time_units = ds.variables['time'].units
        time_calendar = ds.variables['time'].calendar
        time_dates = nc.num2date(
            time_var, units=time_units, calendar=time_calendar)
        index = [i for i, t in enumerate(time_dates) if (
            t.year, t.month, t.day) == (date.year, date.month, date.day)]
        if index:
            precip = ds.variables['precipitationCal'][index[0], :, :]
            precip = np.where(precip == -9999.9, 0, precip)
            sum_matrix += precip
        ds.close()
    all_ppt_2000nn[day_idx, :, :] = sum_matrix

##############____save mat file___############################
mmdd = np.array(mmdd_list, dtype=object)
save_path = r'D:\MS Thesis\Analysis\mmdd_list.mat'
sio.savemat(save_path, {'mmdd_list': mmdd})

data_to_save = {}
for year in range(2000, 2025):
    var_name = f'all_ppt_{year}'
    if var_name in globals():
        data_to_save[var_name] = globals()[var_name]

save_path = r'D:\MS Thesis\Analysis\all_ppt.mat'
sio.savemat(save_path, data_to_save)

# ___load mat precipitation file___$$$
mat_data = loadmat('D:\\MS Thesis\\Analysis\\all_ppt.mat')

# Extract only the actual variables (ignore metadata like __header__)
data_vars = {k: v for k, v in mat_data.items() if not k.startswith('__')}

# Load all variables into global namespace
globals().update(data_vars)

# Convert 'all_ppt' NumPy array to a Python list
ppt = all_ppt.tolist()
###################_____nanmean______###########################

NC_means = {}

for year in range(2000, 2025):
    var_name = f'ppt_{year}_subset'
    if var_name in subset_data():
        data = globals()[var_name].astype(float)
        data[data <= 0] = np.nan
        # Mean over axis (1, 2) -> spatial mean for each time step
        means = np.nanmean(data, axis=(1, 2))
        NC_means[f'mean_ppt_{year}'] = means

savemat('D:\MS Thesis\Analysis\daily_means_separated.mat', daily_means)


###################_____timeseries______#########################

for year in range(2000, 2002):
    key = f'mean_ppt_{year}'

    if key in daily_means:
        y = daily_means[key]

        if len(y) == len(date1):
            x = [f"{year}-{d}" for d in date1]

            plt.figure(figsize=(14, 5))
            plt.plot(x, y, color='royalblue', linewidth=1.5)
            plt.title(
                f'Mean Daily Precipitation - {year}', fontsize=14, weight='bold')
            plt.xlabel('Date (YYYY-MM-DD)', fontsize=12)
            plt.ylabel('Precipitation (mm/hr)', fontsize=12)

            # Display only every 7th date label
            step = 2
            xticks = x[::step]
            xtick_indices = list(range(0, len(x), step))
            plt.xticks(ticks=xtick_indices, labels=xticks,
                       rotation=90, fontsize=9)

            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            plt.show()
        else:
            print(
                f"Length mismatch for {key}: {len(y)} values, {len(date1)} dates.")
    else:
        print(f"{key} not found in daily_means.")
# __colour plpt*********************@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
month_colors = {
    '06': 'gold',          # Yellow
    '07': 'lightskyblue',  # Light blue
    '08': 'lightgreen',    # Light green
    '09': 'lightcoral'     # Light red/pink
}
legend_elements = [
    Line2D([0], [0], color='gold', lw=3, label='June'),
    Line2D([0], [0], color='lightskyblue', lw=3, label='July'),
    Line2D([0], [0], color='lightgreen', lw=3, label='August'),
    Line2D([0], [0], color='lightcoral', lw=3, label='September')
]

for year in range(2000, 2002):
    key = f'mean_ppt_{year}'

    if key in daily_means:
        y = daily_means[key]

        if len(y) == len(date1):
            x = [f"{year}-{d}" for d in date1]

            plt.figure(figsize=(14, 5))
            plt.title(
                f'Mean Daily Precipitation - {year}', fontsize=14, weight='bold')
            plt.xlabel('Date (YYYY-MM-DD)', fontsize=12)
            plt.ylabel('Precipitation (mm/hr)', fontsize=12)

            # Plot each segment by month color
            for i in range(len(x) - 1):  # plot pairwise
                month = date1[i][:2]
                color = month_colors.get(month, 'gray')
                plt.plot(x[i:i+2], y[i:i+2], color=color, linewidth=1.5)

            # Format x-ticks to avoid clutter
            step = 2
            xticks = x[::step]
            xtick_indices = list(range(0, len(x), step))
            plt.xticks(ticks=xtick_indices, labels=xticks,
                       rotation=90, fontsize=9)

            plt.grid(True, linestyle='--', alpha=0.5)

            # Place legend outside the plot
            plt.legend(handles=legend_elements, title="Month", bbox_to_anchor=(
                1.02, 1), loc='upper left', borderaxespad=0.)

            # adjust layout to make room for legend
            plt.tight_layout(rect=[0, 0, 0.85, 1])
            plt.show()
        else:
            print(
                f"Length mismatch for {key}: {len(y)} values, {len(date1)} dates.")
    else:
        print(f"{key} not found in daily_means.")