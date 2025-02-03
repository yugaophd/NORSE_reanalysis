
import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('/home/yugao/projects/NORSE_reanalysis/src')

# Load the data
ds = xr.open_dataset('../data/external/cmems_mod_glo_phy_myint_0.083deg_P1D-m_1738611987452.nc')
ds

# %%
# Use xr.resample() to make T(x,z,t) for sections 
# from 71.211565N, 6.298711W to 70.836847N, 6.411678W

T = ds.thetao
T_section = T.sel(latitude=slice(71.211565, 70.836847), longitude=slice(-6.411678, -6.298711))

# %%
T_section.data
# %%
import xarray as xr
import numpy as np

# Define the start and end points of the section
start_lat, start_lon = 71.211565, -6.298711  # Convert W to negative longitude
end_lat, end_lon = 70.836847, -6.411678

# Number of points along the section
num_points = 100

# Generate latitudes and longitudes along the section
latitudes = np.linspace(start_lat, end_lat, num_points)
longitudes = np.linspace(start_lon, end_lon, num_points)

# Interpolate along the section
ds_section = ds.interp(latitude=("points", latitudes), longitude=("points", longitudes))

# Resample in time
ds_resampled = ds_section #.resample(time="1D").mean()

# Visualize the result or save
print(ds_resampled)


# %%
# Plot the section in full ocean depth


import matplotlib.pyplot as plt

# Extract data from the dataset
# Temperature section

thetao = ds_resampled['thetao']
time = thetao['time']
depth = thetao['depth']
latitude = thetao['latitude']
longitude = thetao['longitude']

max_depth = thetao['depth'].max().values  # Maximum depth in the dataset

# Create the plots for the full ocean depth
for t, tt in enumerate(time.data):
    
    # Convert latitude and longitude to a string format for labeling
    lat_lon_labels = [f"{lat:.2f}°N, {lon:.2f}°W" for lat, lon in zip(latitude.values, longitude.values)]

    # Create the plot
    plt.figure(figsize=(14, 6))
    for t in range(len(time)):
        plt.contourf(
            latitude,
            -depth,
            thetao.isel(time=t),
            levels=50,
            cmap='viridis'
        )

    # Add labels and titles
    plt.ylim(-2600, 0)  # Reverse the y-axis to show depth increasing downwards
    plt.colorbar(label="Potential Temperature (°C)")
    plt.xticks(latitude[0::10], labels=lat_lon_labels[0::10], rotation=45, ha="right")  # Use lat/lon labels
    plt.xlabel("Latitude, Longitude")
    plt.ylabel("Depth (m)")
    plt.title(f"Temperature from (71.211565N, 6.298711W) to (70.836847N, 6.411678W) {tt}", fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.savefig(f'../data/processed/UTS_section_full_{tt}.png')


# %%
# plot the upper ocean
max_depth = 300  # Define the depth range (e.g., upper 300 meters)

thetao_upper = ds_resampled['thetao'].sel(depth=slice(0, max_depth))  # Slice depths

# Extract the necessary dimensions
depth = thetao_upper['depth']
latitude = thetao_upper['latitude']
longitude = thetao_upper['longitude']
time = thetao_upper['time']

# Create the plots for the upper ocean
for t, tt in enumerate(time.data):
    # Combine latitude and longitude into labels for the x-axis
    lat_lon_labels = [f"{lat:.2f}°N, {-lon:.2f}°W" for lat, lon in zip(latitude.values, longitude.values)]

    # Create the plot
    plt.figure(figsize=(14, 6))
    for t in range(len(time)):
        plt.contourf(
            latitude,
            -depth,  # Negative depth for proper orientation
            thetao_upper.isel(time=t),
            levels=50,
            cmap='viridis'
        )

    # Add colorbar, labels, and titles
    plt.colorbar(label="Potential Temperature (°C)")
    plt.xticks(latitude[0::10], labels=lat_lon_labels[0::10], 
            rotation=45, ha="right")  # Use lat/lon labels
    plt.xlabel("Latitude, Longitude")
    plt.ylabel("Depth (m)")
    plt.title(f"Temperature from (71.211565N, 6.298711W) to (70.836847N, 6.411678W) {tt} ") # (Upper {max_depth}m)

    # Adjust layout and show plot
    plt.tight_layout()
    plt.savefig(f'../data/processed/UTS_section_upper_{max_depth}m_{tt}.png')

# %%
