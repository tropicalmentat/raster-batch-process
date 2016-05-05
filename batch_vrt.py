import os
import glob
from subprocess import call

def list_raster(indir):

    tif_list = glob.glob(indir+'\clip3*.TIFF')
    with open(indir+'\\tif_list.txt', 'wb') as f:
        for fn in tif_list:
            path, name = os.path.split(fn)
            print fn
            f.writelines(fn+'\n')
    return

def build_vrt(indir):
    
    list_dir = glob.glob(indir+'\*.txt')
    print '\nfound %s in %s' % (list_dir[0], indir)
    print '\nbuilding vrt...'
    ndvi_anom = indir+"\\ndvi_2001-2010.vrt"
    vrt_make = ["gdalbuildvrt", "-separate", "-input_file_list", list_dir[0], ndvi_anom]
    call(vrt_make)
    
    return

def main():
    work_dir = "D:\\LUIGI\\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\\RAINFALL\\new_rainfall_images\\15-16_anomaly"
    ras_list = glob.glob(work_dir+'\*.TIFF')

    for root, dirs, files in os.walk(work_dir):
        #print root
        for f in files:
            if '.TIFF' in f:
                file_path = root+'\\'+f
                list_raster(work_dir)
                build_vrt(work_dir)

if __name__ == "__main__":
    main()
