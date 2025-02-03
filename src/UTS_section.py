
import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('/Users/yugao/Desktop/projects/NORSE_reanalysis/src')

# Load the data
ds = xr.open_dataset('../data/external/cmems_mod_glo_phy_myint_0.083deg_P1D-m_1738594404593.nc')
ds

# %%
# Use xr.resample() to make T(x,z,t) for sections from 71.211565N, 6.298711W to 70.836847N, 6.411678W
