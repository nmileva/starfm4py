# -*- coding: utf-8 -*-

import time
import rasterio
import numpy as np
import starfm4py as stp
import matplotlib.pyplot as plt
from parameters import (path, sizeSlices)
#import dask.array as da
#import scipy, scipy.signal



start = time.time()

#Set the path where the stacked images are stored
#with rasterio.open('C:/Users/Nikolina Mileva/Documents/Data/subset_10km_20170712_20180714.tif') as product:
#    profile = product.profile
#    Sentinel2T0 = product.read(1)
#    Sentinel3T0 = product.read(5)*10000
#    Sentinel3T1 = product.read(10)*10000

#with rasterio.open('C:/Users/Nikolina Mileva/Desktop/LMSS_comparison/subset_S3A_S2A_B8A_new.tif') as product:
#    Sentinel2T0 = product.read(3)#/10000.0 #np.arange(100000000).reshape((10000,10000))#
#    print (np.nanmean(Sentinel2T0))

#with rasterio.open('C:/Users/Nikolina Mileva/Desktop/LMSS_comparison/subset_S2A_S3A_B2.tif') as product:
#    profile = product.profile
#    Sentinel2T0 = product.read(1)#/10000.0 #np.arange(100000000).reshape((10000,10000))#
#    print (np.nanmean(Sentinel2T0))
#    Sentinel3T0 = product.read(3)#/10000.0#  np.arange(100000000).reshape((10000,10000))#
#    print (np.nanmean(Sentinel3T0))
#    Sentinel3T1 = product.read(4)#/10000.0 #np.arange(100000000).reshape((10000,10000))#
#    print (np.nanmean(Sentinel3T1))
    

    


product = rasterio.open('C:/Users/Nikolina Mileva/Desktop/SPIE paper/Illustrations/Test_case_3/sim_Landsat_t1.tif')
profile = product.profile
Sentinel2T0 = rasterio.open('C:/Users/Nikolina Mileva/Desktop/SPIE paper/Illustrations/Test_case_3/sim_Landsat_t1.tif').read(1)
print ("Sentinel2T0 ", Sentinel2T0.shape)
print (Sentinel2T0.dtype)
Sentinel3T0 = rasterio.open('C:/Users/Nikolina Mileva/Desktop/SPIE paper/Illustrations/Test_case_3/sim_MODIS_t1.tif').read(1)
print ("Sentinel3T0 ", np.mean(Sentinel3T0))
print (Sentinel3T0.dtype)
Sentinel3T1 = rasterio.open('C:/Users/Nikolina Mileva/Desktop/SPIE paper/Illustrations/Test_case_3/sim_MODIS_t4.tif').read(1)
print ("Sentinel3T1 ", np.mean(Sentinel3T1))
print (Sentinel3T1.dtype)


path_fineRes_t0 = 'Temporary/Tiles_fineRes_t0/'
path_coarseRes_t0 = 'Temporary/Tiles_coarseRes_t0/'
path_coarseRes_t1 = 'Temporary/Tiles_fcoarseRes_t1/'



fine_image_t0_par = stp.partition(Sentinel2T0, path_fineRes_t0)
coarse_image_t0_par = stp.partition(Sentinel3T0, path_coarseRes_t0)
coarse_image_t1_par = stp.partition(Sentinel3T1, path_coarseRes_t1)


print ("Done partitioning!")

#fine_image_t0 = stp.da_stack(path_fineRes_t0, Sentinel2T0.shape)
#print (fine_image_t0.shape)
#coarse_image_t0 = stp.da_stack(path_coarseRes_t0, Sentinel3T0.shape)
#print (coarse_image_t0.shape)
#coarse_image_t1 = stp.da_stack(path_coarseRes_t1, Sentinel3T1.shape)
#print (coarse_image_t1.shape)


S2_t0 = stp.da_stack(path_fineRes_t0, Sentinel2T0.shape)#[1339560:2679120,]#[119220930:120560490,]
S3_t0 = stp.da_stack(path_coarseRes_t0, Sentinel3T0.shape)#[1339560:2679120,]#[119220930:120560490,]
S3_t1 = stp.da_stack(path_coarseRes_t1, Sentinel3T1.shape)#[1339560:2679120,]#[119220930:120560490,]


shape = (sizeSlices, Sentinel2T0.shape[1])

print ("Done stacking!")

#predictions = stp.starfm(S2_t0, S3_t0, S3_t1, profile, Sentinel2T0.shape) # for small images

for i in range(0, Sentinel2T0.size-sizeSlices*shape[1]+1, sizeSlices*shape[1]):
    
    fine_image_t0 = S2_t0[i:i+sizeSlices*shape[1],]
    coarse_image_t0 = S3_t0[i:i+sizeSlices*shape[1],]
    coarse_image_t1 = S3_t1[i:i+sizeSlices*shape[1],]
    prediction = stp.starfm(fine_image_t0, coarse_image_t0, coarse_image_t1, profile, shape)
    
    if i == 0:
        predictions = prediction
        
    else:
        predictions = np.append(predictions, prediction, axis=0)
  

# Write the results to a .tif file   
print ('Writing product...')
profile = product.profile
profile.update(dtype='float64', count=1) # number of bands
file_name = path + 'prediction.tif'

result = rasterio.open(file_name, 'w', **profile)#rasterio.open(file_name, 'w', **defaults(count=1))# 
result.write(predictions, 1)
result.close()


end = time.time()
print ("Done in", (end - start)/60.0, "minutes!")

# Display input and output
plt.imshow(Sentinel2T0)
plt.gray()
plt.show()
plt.imshow(Sentinel3T0)
plt.gray()
plt.show()
plt.imshow(Sentinel3T1)
plt.gray()
plt.show()	
plt.imshow(result)
plt.gray()
plt.show()
