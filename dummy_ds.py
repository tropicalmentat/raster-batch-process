__author__ = 'G Torres'
"""Script to create dummy raster based based on the minimum and
maximum of a multi-dimensional array data-set. This will be used
for creating a fixed scale for GIS visualization in ArcGIS"""

import os
import gdal
from gdalconst import *
import numpy as np

gdal.AllRegister()

def build_dummy(fpath):
    
    ras = gdal.Open(fpath, GA_ReadOnly)
    gt, proj = ras.GetGeoTransform(), ras.GetProjection()
    cols, rows = ras.RasterXSize, ras.RasterYSize
    num_band = ras.RasterCount

    array_list = []
    # collect list of band array objects
    for i in range(1, num_band):
        array_list.append(ras.GetRasterBand(i).
                          ReadAsArray(0,0,cols,rows))
    array_stack = np.dstack(array_list)  # create multi-dim array from list
    dummy_shape = array_list[0].shape  # retrieve shape from a sample array
    min, max = int(np.amin(array_stack)), int(np.amax(array_stack))  # retrieve min and max
    dummy_array = np.random.randint(-10, 110, dummy_shape)  # create dummy array
    print dummy_array

    # create output raster data-set
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()
    out_ras = driver.Create("dummy_ds.tif", cols, rows, 1, GDT_Int16)
    out_ras.SetProjection(proj)
    out_ras.SetGeoTransform(gt)
    out_band = out_ras.GetRasterBand(1)
    out_band.WriteArray(dummy_array,0,0)
    out_band.FlushCache()

    return


def main():
    work_dir = "D:\\LUIGI\\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\\RAINFALL\\new_rainfall_images\\15-16_anomaly"

    for root, dirs, files in os.walk(work_dir):
        #print root
        for f in files:
            if '.vrt' in f:
                file_path = root+'\\'+f
                build_dummy(file_path)

if __name__ == "__main__":
    main()
