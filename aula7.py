#%% Importando módulos
import numpy as np
import imageio
from medImUtils import imUtils
import cv2
import os

#%% 1 - Ultrassom bebe
cf = os.getcwd() # current folder
I1_path = os.path.join(cf,'ImagensAulas','Ultrassom.pgm') # endereco da imagem
I1 = imUtils.uint2double(imageio.imread(I1_path))

rect = cv2.selectROI(I1) # selecionando região de interesse com openCV
# Selecionar a região e dar enter 2x
cv2.waitKey(0)
cv2.destroyAllWindows()
c1,c2 = rect[0],rect[0]+rect[2] # coluna minima e coluna maxima
l1,l2 = rect[1],rect[0]+rect[3] # linha minima e linha maxima

meanRect = np.mean(I1[l1:l2,c1:c2])
stdRect = np.std(I1[l1:l2,c1:c2])
#%% Filtro de Lee (essa demora)
image = I1
kernelLength = 7
newImage = np.zeros(image.shape)
w = np.zeros((kernelLength,kernelLength),dtype=int)
w_center = int((w.shape[0])/2)
for indexrow,frow in enumerate(image[:-(w_center*2)]):
    for indexcolumn,fcolumn in enumerate(frow[:-(w_center*2)]): 
        maskLocal = image[indexrow:1+indexrow+w_center*2,indexcolumn:1+indexcolumn+w_center*2]
        meanMask = np.mean(maskLocal + w)
        k = np.clip(1-(stdRect/(0.001 + maskLocal.std())),0,1) # minimo é zero e maximo é 1
        newImage[indexrow+w_center,indexcolumn+w_center] = meanMask + k*(image[indexrow+w_center,indexcolumn+w_center] - meanMask)
        
imUtils.showImageStyle(1,2,{'I1':imUtils.im2uint8(I1),'newImage':imUtils.im2uint8(newImage)},['Original','Image Filtered'])
#%% Função zero bala Filtro de Lee (esse é rapidaooooo)
newImage = imUtils.LeeFilter(I1,9,True)

#%% DESAFIO
sobel_Image = imUtils.im2double(imUtils.sobel(I1))
meanI1 = imUtils.im2double(imUtils.meanFilterFast(I1,11))
challenge = meanI1 + sobel_Image*(I1-meanI1)
imUtils.showImageStyle(1,2,{'I1':imUtils.im2uint8(I1),'challenge':imUtils.im2uint8(challenge)},['Original','Challenge'])


