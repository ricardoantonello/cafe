import cv2
import numpy as np
#imports para PICamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from matplotlib import pyplot as plt

def histogramaRGB(img):
    #Separa os canais
    canais = cv2.split(img)
    cores = ("b", "g", "r")
    fig = plt.figure()
    plt.title("'Histograma Colorido")
    plt.xlabel("Intensidade")
    plt.ylabel("Número de Pixels")
    for (canal, cor) in zip(canais, cores):
        #Este loop executa 3 vezes, uma para cada canal
        hist = cv2.calcHist([canal], [0], None, [256], [0, 256])
        plt.plot(hist, color = cor)
        plt.xlim([0, 256])
    # If we haven't already shown or saved the plot, then we need to
    # draw the figure first...
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data

def histogramaHSV(img):
    #Separa os canais
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    canais = cv2.split(hsv)
    cores = ("m", "c", "y")
    fig = plt.figure()
    plt.title("'Histograma HSV")
    plt.xlabel("Intensidade")
    plt.ylabel("Número de Pixels")
    for (canal, cor) in zip(canais, cores):
        #Este loop executa 3 vezes, uma para cada canal
        hist = cv2.calcHist([canal], [0], None, [256], [0, 256])
        plt.plot(hist, color = cor)
        plt.xlim([0, 256])
    # If we haven't already shown or saved the plot, then we need to
    # draw the figure first...
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data

def imprime_cor(img): #imagem deve estar em formato RGB
    blue = 0
    for p in np.ravel(img[::4,::4,0]):
       blue+=p
    green = 0
    for p in np.ravel(img[::4,::4,1]):
       green+=p
    red = 0
    for p in np.ravel(img[::4,::4,2]):
       red+=p
    print('red:',red,' green:',green,' blue:',blue, end='')

    hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
    h = 0
    for p in np.ravel(hsv[::4,::4,0]):
       h+=p
    s = 0
    for p in np.ravel(hsv[::4,::4,1]):
       s+=p
    v = 0
    for p in np.ravel(hsv[::4,::4,2]):
       v+=p
    print('       hue:',h,' saturation:', s,' value:', v)



def encontra_cor(img): #imagem deve estar em formato RGB
    red = 0
    for p in np.ravel(img[::4,::4,0]):
        if p>100:
            red+=1
    green = 0
    for p in np.ravel(img[::4,::4,1]):
        if p>100:
            green+=1
    blue = 0
    for p in np.ravel(img[::4,::4,2]):
        if p>100:
            blue+=1

    #print('r',red,'g',green,'b',blue)
    if red>green and red>blue:
        return "Vermelho"+','+str(red)+','+str(green)+','+str(blue)
    elif green>red and green>blue:
        return "Verde"+','+str(red)+','+str(green)+','+str(blue)
    elif blue>red and blue>green:
        return "Azul"+','+str(red)+','+str(green)+','+str(blue)
    else:
        return ''+','+str(red)+','+str(green)+','+str(blue)

def texto(img, texto, coord, fonte = cv2.FONT_HERSHEY_SIMPLEX, cor=(0,0,255), tamanho=0.7, thickness=2):
    textSize, baseline = cv2.getTextSize(texto, fonte, tamanho, thickness);
    cor_background = 0
    if type(cor)==int: # se não for colorida a imagem
        cor_background=255-cor
    else:
        cor_background=(255-cor[0],255-cor[1],255-cor[2])
    #print(cor_background)
    cv2.rectangle(img, (coord[0], coord[1]-textSize[1]-3), (coord[0]+textSize[0], coord[1]+textSize[1]-baseline), cor_background, -1)
    #cv2.putText(img, texto, coord, fonte, tamanho, cor_background, thickness+1, cv2.LINE_AA)
    cv2.putText(img, texto, coord, fonte, tamanho, cor, thickness, cv2.LINE_AA)
    return img

if __name__ == '__main__':

    #PARA USAR COM CAMERA USB
    #vc = cv2.VideoCapture(0)
    #vc.set(cv2.CAP_PROP_FRAME_WIDTH,320)  
    #vc.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    #if vc.isOpened(): # try to get the first frame
    #    is_capturing, frame = vc.read()
    #else:
    #    is_capturing = False  

    #PARA USAR COM CAMERA PI
    camera = PiCamera()
    #camera.resolution = (640, 480) # sequiser mudar a resolução padrao
    #camera.resolution = (320, 240) # sequiser mudar a resolução padrao
    #camera.resolution = (1920, 1080) # sequiser mudar a resolução padrao
    #camera.framerate = 32
    rawCapture = PiRGBArray(camera)  # , size=(320, 240))
    # allow the camera to warmup
    time.sleep(0.1)

    primeiro_frame = 0
    #while is_capturing:
    roi = [] # cria variável roi
    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True): # para uso com Pi Camera
        
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame = frame.array
        #frame = frame.copy()

        #No Primeiro Frame faz a calibragem do ROI (Region of Interest)
       
        if primeiro_frame == 0:
            primeiro_frame = 1
            roi = cv2.selectROI(frame[::2,::2,::-1]) #diminui a imagem para escolher regiao de interesse
            roi = (roi[0]*2, roi[1]*2, roi[2]*2, roi[3]*2)
            print('>> ROI:', roi)
            cv2.destroyAllWindows()
          
        #aplica ROI em todos os frames do primeiro em diante
        frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        img_width, img_height = frame.shape[1], frame.shape[0] 
        #print('Shape:', img_width, img_height)

        try:    # Lookout for a keyboardInterrupt to stop the script
            #is_capturing, frame = vc.read()   # somente para camera USB

            #frame = cv2.resize(frame[:,:,::-1], (320,240))

            frameRGB = frame[:,:,::-1] # inverte BGR para RGB
            #cor = encontra_cor(frame)
            
            frameBGR = frame.copy()
            #frame = texto(frame.copy(), cor, (10,25))
            
            imprime_cor(frameBGR.copy())
            histRGB = histogramaRGB(frameBGR.copy())
            histRGB = cv2.resize(histRGB.copy(), (320,240), interpolation = cv2.INTER_AREA)
            histHSV = histogramaHSV(frameBGR.copy())
            histHSV = cv2.resize(histHSV.copy(), (320,240), interpolation = cv2.INTER_AREA)
            size = (histRGB.shape[1], histRGB.shape[0])
            frameRGB_res = cv2.resize(frameRGB, size, interpolation = cv2.INTER_AREA)
            frameBGR_res = cv2.resize(frameBGR, size, interpolation = cv2.INTER_AREA)
            join = np.vstack([
                np.hstack([frameRGB_res, frameBGR_res]),
                np.hstack([histRGB, histHSV]),
            ])

            window_name = "Cafe"
            #cv2.namedWindow(window_name, flags=cv2.WND_PROP_FULLSCREEN);
            #cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            #cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, join) #converte para BGR para mostrar
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0) # para uso com Pi Camera
        
        except KeyboardInterrupt:
            # vc.release() # só usado com camera USB
            cv2.destroyAllWindows()


