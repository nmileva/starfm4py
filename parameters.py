import numpy as np



# Set the size of the moving window in which the search for similar pixels 
# is performed
windowSize = 31

# Set the path where the results should be stored
path = 'C:/Users/Nikolina Mileva/Desktop/STARFM_demo/'

# Set to True if you want to decrease the sensitivity to the spectral distance
logWeight = False

# If more than one training pairs are used, set to True
# Check line 332 from StarFM_compute.c
temp = False

# The spatial impact factor is a constant defining the relative importance of 
# spatial distance (in meters)
# Take a smaller value of the spatial impact factor for heterogeneous regions 
# (e.g. A = 150 m)
spatImp = 150 # default 450; 150 for heterogeneous areas; 25 cuSTARFM

# increasing the number of classes limits the number of similar pixels
numberClass = 4 

# Set the uncertainty value for the fine resolution sensor
# https://earth.esa.int/web/sentinel/technical-guides/sentinel-2-msi/performance 
uncertaintyFineRes = 0.03

# Set the uncertainty value for the coarse resolution sensor
# https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-3-olci/validation
uncertaintyCoarseRes = 0.03 #0.025 

# Other global variables
mid_idx = (windowSize**2)//2
specUncertainty = np.sqrt(uncertaintyFineRes**2 + uncertaintyCoarseRes**2)
tempUncertainty = np.sqrt(2*uncertaintyCoarseRes**2)

# Set number of slices in which the image to be devided
numSlices = 1720#1146 #3247 #1021# increase the number for smaller images, should be multiple of the image height





