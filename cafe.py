import cv2
import numpy as np

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
        return "Verdade"+','+str(red)+','+str(green)+','+str(blue)
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

    vc = cv2.VideoCapture(0)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH,320)  
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    if vc.isOpened(): # try to get the first frame
        is_capturing, frame = vc.read()
    else:
        is_capturing = False  

    while is_capturing:
        try:    # Lookout for a keyboardInterrupt to stop the script
            is_capturing, frame = vc.read()   

            #frame = cv2.resize(frame[:,:,::-1], (320,240))

            frame = frame[:,:,::-1] # inverte BGR para RGB
            cor = encontra_cor(frame)
            #print(cor)
            frame = texto(frame.copy(), cor, (10,25))
            window_name = "Cafe"
            #cv2.namedWindow(window_name, flags=cv2.WND_PROP_FULLSCREEN);
            #cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            #cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            frame = frame[:,:,::-1] # inverte BGR para RGB
            cv2.imshow(window_name, frame) #converte para BGR para mostrar
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        except KeyboardInterrupt:
            vc.release()
            cv2.destroyAllWindows()


