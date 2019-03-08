from PIL import Image, ImageChops

def isWidespread(img):
        # Recortamos el margen que separa las dos mitades de la imagen
        middle_crop = getMiddleSeparation(img,25)

        # Eliminamos el polvo y convertimos los colores a BW
        middle_crop = cleanDusk(middle_crop)

        #Si no es un margen solido entonces quizas se trate de un widespread
        if not isSolidColor(middle_crop):

            #Cortamos la separacion en dos para analizar cada una con mas detalle
            left, right = getImageHalves(middle_crop)

            #Si una de las mitades es completamente solida, lo mas probable es que sea una composicion de paginas individuales y no un widespread
            return not isSolidColor(left) and not isSolidColor(right)
        else:
            ##Si la separacion central es completamente solida entonces lo mas probable es que no se trate de un widespread
            return False

def getMiddleSeparation(img,separation_size=50):
        middle_point = int(img.width/2)

        half_size = int(separation_size)

        left = middle_point - half_size
        top = 0
        right = middle_point + half_size
        bottom = img.height

        return img.crop((left,top,right,bottom))

def cleanDusk(img, threshold = 50):
        # Convertimos en negro los puntos de la imagen por debajo de cierto threshold y en blanco el resto
        img = img.convert('L')
        return img.point(lambda x: 0 if x<threshold else 255, '1')

def isSolidColor(img):
        return not ImageChops.invert(img).getbbox() or not img.getbbox()

def getImageHalves(img):
        middle_point = int(img.width/2)

        half_l = img.crop((0,0,middle_point,img.height))
        half_r = img.crop((middle_point,0,img.width,img.height))

        return half_l,half_r







