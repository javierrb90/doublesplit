from PIL import Image
import zipfile, shutil, os, sys
from os.path import basename
from . import progressbar, pageparser

PATH_TEMP = "temp"

def parseComic(path_comic):

    createTempFolder(PATH_TEMP)

    with zipfile.ZipFile(path_comic) as thezip:
        count = 0

        newlist = sorted(thezip.filelist, key=lambda x: x.filename, reverse=False)

        total = len(newlist)+1
        i=0

        for thefile in newlist:
            i+=1
            count = parseComicPage(thezip=thezip,thefile=thefile,count=count)
            progressbar.print_progress(i,total)
            
    new_package_name = thezip.filename+"_new."+getExtension(thezip.filename)

    createPackage(path_comic=new_package_name, path_files=PATH_TEMP, callback=cleanTempFolder)

    progressbar.print_progress(total,total)

def parseComicPage(**kwargs):

    thezip = kwargs['thezip']
    thefile = kwargs['thefile']
    count = kwargs['count']

    if not thefile.is_dir():
    # Solamente nos interesan las imagenes, ignoramos el resto
        try:
            img = Image.open(thezip.open(thefile.filename))
        except OSError:
            return count

        halves = [img]

        if img.width > img.height:
            if not pageparser.isWidespread(img):
                half_l, half_r = pageparser.getImageHalves(img)
                halves = [half_r,half_l]

        for half in halves:
            count+=1
            new_page_path = PATH_TEMP+"/"+getNewPageName(count,thefile.filename)

            half.save(new_page_path,optimize=True)

    return count

def getNewPageName(number,filename,zeroes=3):
    return str(number).zfill(zeroes)+"."+getExtension(filename)

def getExtension(filename):
    return filename.split(".")[-1]


def createTempFolder(path_temp):
    cleanTempFolder(path_temp)
    if not os.path.exists(path_temp):
        os.makedirs(path_temp)

def cleanTempFolder(path_temp):
    shutil.rmtree(path_temp, ignore_errors=True)

def createPackage(path_comic,path_files,callback=None):

    files = [path_files+"/"+f for f in os.listdir(path_files)]

    with zipfile.ZipFile(path_comic,"w",zipfile.ZIP_DEFLATED) as thecbz:
        for thefile in files:
            
            thecbz.write(thefile,basename(thefile))
    
    if(callback is not None):
        callback(path_files)