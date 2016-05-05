import os
import glob
import gdal
from gdalconst import *
import numpy as np
import matplotlib as mlab
import matplotlib.pyplot as plt


def build_astack(fpath):
    
    ras = gdal.Open(fpath, GA_ReadOnly)
    cols, rows = ras.RasterXSize, ras.RasterYSize
    num_band = ras.RasterCount

    array_list = []
    for i in range(1, num_band):
        array_list.append(ras.GetRasterBand(i).
                          ReadAsArray(0,0,cols,rows))

    array_stack = np.dstack(array_list)
    flat_stack = array_stack.flatten()
    print np.amin(array_stack), np.std(array_stack), np.amax(array_stack), '\n'
    for i in array_list:
        print np.amin(i), np.std(i), np.amax(i)

    plt.hist(flat_stack, bins=50)
    plt.xlabel('pixel values')
    plt.ylabel('number of pixels')
    plt.show()

    return


def main():
    work_dir = "D:\\LUIGI\\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\\RAINFALL\\new_rainfall_images\\15-16_anomaly"

    for root, dirs, files in os.walk(work_dir):
        #print root
        for f in files:
            if '.vrt' in f:
                file_path = root+'\\'+f
                build_astack(file_path)

if __name__ == "__main__":
    main()
