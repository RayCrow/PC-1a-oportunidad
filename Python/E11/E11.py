def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        #Parse geo references.
        Nsec = exif['GPSInfo'][2][2] 
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][3] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)

def get_exif_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret

def PrintMeta(dire):
    print("Ruta de imágenes: "+dire)
    os.chdir(dire)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            print(os.path.join(root, name))
            print ("[+] Metadata for file: %s " %(name))
            try:
                exifData = {}
                exif = get_exif_metadata(name)
                for metadata in exif:
                    print ("Metadata: %s - Value: %s " %(metadata, exif[metadata]))
                print ("\n")
            except:
                import sys, traceback, PIL
                traceback.print_exc(file=sys.stdout)

def MetaSingleImg(imagep):
    print('\n[+] Metadata for file: %s ' %(imagep))
    try:
        exifData = {}
        exif = get_exif_metadata(imagep)
        for metadata in exif:
            print ("Metadata: %s - Value: %s " %(metadata, exif[metadata]))
        print ("\n")
    except:
        import sys, traceback, PIL
        traceback.print_exc(file=sys.stdout)

def MetaUrl(url):
    furl = []
    pathhh = os.getcwd()
    r  = requests.get("http://" +url)
    data = r.text
    soup = BeautifulSoup(data,'html.parser')
    for link in soup.find_all('img'):
        if link is not None:
            furl.append(link.get('src'))
    arrlenght = len(furl)
    arrlenght = arrlenght - 1
    numarch = 0
    for i in range(0,arrlenght,1):
        imgurl = furl[i]
        nombreimg = 'imagen'+str(numarch)+'.jpg'
        imagen = requests.get(imgurl).content
        with open(nombreimg, 'wb') as handler:
            handler.write(imagen)
        with urllib.request.urlopen(imgurl) as i:
            fpath = io.BytesIO(i.read())
        print ("[+] Metadata for file: %s " %(imgurl))
        print ('Se va a guardar en: ','imagen'+str(numarch)+'.txt')
        try:
            exifData = {}
            exif = get_exif_metadata(fpath)
            for metadata in exif:
                archivo = 'imagen'+str(numarch)+'.txt'
                files = open(pathhh+'\\'+archivo, 'w')
                files.write("Metadata: %s - Value: %s " %(metadata, exif[metadata]))
                files.close()
                print(("Metadata: %s - Value: %s " %(metadata, exif[metadata])))
            print ("\n")
        except:
            import sys, traceback, PIL
            traceback.print_exc(file=sys.stdout)
        numarch += 1

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', help='Ingresar link de pagina web a analizar')
    parser.add_argument('-p', help='Ingresar el path de la foto')
    parser.add_argument('-dp', help='Ingresar path de la carpeta donde hay multiples fotos')
    args = parser.parse_args()
    if args.l:
        MetaUrl(args.l)
    elif args.p:
        PrintMeta(args.p)
    elif args.dp:
        MetaSingleImg(args.dp)
    else:
        print(parser.usage)

if __name__ == '__main__':
    try:
        from PIL.ExifTags import TAGS, GPSTAGS
        from PIL import Image, ImageFilter
        import os
        from bs4 import BeautifulSoup
        import requests
        import urllib.request,io
        import argparse
        Main()
    except ImportError:
        import os
        print("Error on Packages","Installing Packages")
        os.system('pip install -r requirements.txt')
        print("Packages Installed","ReRun")
        exit()