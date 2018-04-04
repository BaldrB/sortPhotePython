import os
import datetime
import time
import piexif
import shutil

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def sortfile(pathfilesout, pathfilesin):
    """Поиск даты в exif"""

    cou_folder = 0
    cou_files = 0

    cou = 0
    cou_f = 0
    pathall = []

    for path, dirs, files in os.walk(pathfilesout):
        pathall.append(path)
    cou_folder = len(pathall)

    for pathfile in pathall:
        faile = os.listdir(pathfile)
        faile = list(filter(lambda x: x.endswith('.jpg') or x.endswith('.jpg'), faile))
        gm = ''
        cou_files = len(faile)
        cou_f += 1
        cou = 0
        for i in faile:
            exif_dict = piexif.load(os.path.join(pathfile, i))
            ls = os.path.getsize(os.path.join(pathfile, i))
            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[ifd]:
                    if ((piexif.TAGS[ifd][tag]["name"] == "DateTime") or (piexif.TAGS[ifd][tag]["name"] == "DateTimeOriginal")):  
                        gm = exif_dict[ifd][tag]
            if(gm != None):
                gm = gm.decode("utf-8")
                gm = gm.replace(':', '.')
                gm = gm[0:7]
            os.system('cls' if os.name == 'nt' else 'clear')
            cou += 1
            print('Папка', cou_f, 'из', cou_folder)
            print('Файл номер', cou, 'из', cou_files)
            if(os.path.exists(os.path.join(pathfilesin, gm))):
                shutil.copy(os.path.join(pathfile,i), os.path.join(pathfilesin,gm))
            else:
                os.mkdir(os.path.join(pathfilesin, gm))
                shutil.copy(os.path.join(pathfile,i), os.path.join(pathfilesin,gm))
    print('ok')


d = modification_date('img1.jpg')
print(d)
f = os.stat('img1.jpg').st_mtime
print(datetime.datetime.fromtimestamp(f))
f = os.stat('img1.jpg').st_ctime
print(datetime.datetime.fromtimestamp(f))
f = os.stat('img1.jpg').st_atime
f = str(datetime.datetime.fromtimestamp(f))
print(f[:7])
gm = b''
exif_dict = piexif.load(os.path.join("img1.jpg"))
for ifd in ("0th", "Exif", "GPS", "1st"):
    for tag in exif_dict[ifd]:
         if ((piexif.TAGS[ifd][tag]["name"] == "DateTime") or (piexif.TAGS[ifd][tag]["name"] == "DateTimeOriginal")):  
            gm = exif_dict[ifd][tag]
            
print(gm.decode("utf-8"))

if gm != b'':
    gm = gm.decode("utf-8")
else:
    gm = '0000.0'
print(gm)