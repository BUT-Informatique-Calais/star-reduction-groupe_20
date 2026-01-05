###############################
# TEST modification du noyaux #
###############################

from astropy.io import fits
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import os 


def multiErosionKernel(fitsFile: str, nbErosion: int, tailleKernel: int)->None :
    """applique l'erosion plusieur fois 

    Args:
        fitsFile (str): le chemin du fichier .fits
        nbErosion (int): le nombre d'erosion
    """
    # Open and read the FITS file
    hdul = fits.open(fitsFile)
    
    # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
    fileName = fitsFile.split("/")[-1].removesuffix(".fits") 
    
    # on crée le dossier des résultat : 
    os.makedirs("resultsMultiErosionKernel", exist_ok=True)
    os.makedirs("resultsMultiErosionKernel/kernel" + str(tailleKernel) + "_" + fileName, exist_ok=True)


    # Access the data from the primary HDU
    data = hdul[0].data

    # Access header information
    header = hdul[0].header

    # Handle both monochrome and color images
    if data.ndim == 3:
        # Color image - need to transpose to (height, width, channels)
        if data.shape[0] == 3:  # If channels are first: (3, height, width)
            data = np.transpose(data, (1, 2, 0))
        # If already (height, width, 3), no change needed
        
        # Normalize the entire image to [0, 1] for matplotlib
        data_normalized = (data - data.min()) / (data.max() - data.min())
        
        # Save the data as a png image (no cmap for color images)
        plt.imsave('./resultsMultiErosionKernel/kernel' + str(tailleKernel) + "_" + fileName + '/original.png', data_normalized)
        
        # Normalize each channel separately to [0, 255] for OpenCV
        image = np.zeros_like(data, dtype='uint8')
        for i in range(data.shape[2]):
            channel = data[:, :, i]
            image[:, :, i] = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype('uint8')
    
        # Passage de RGB a BGR 
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    else:
        # Monochrome image
        plt.imsave('./resultsMultiErosionKernel/kernel' + str(tailleKernel) + "_" + fileName + '/original.png', data, cmap='gray')
        
        # Convert to uint8 for OpenCV
        image = ((data - data.min()) / (data.max() - data.min()) * 255).astype('uint8')



    # Define a kernel for erosion
    kernel = np.ones((tailleKernel, tailleKernel), np.uint8)

    print("création erosion pour " + fileName + "...")
    # boucle 
    for i in range(nbErosion): 
        # Perform erosion
        eroded_image = cv.erode(image, kernel, iterations=i + 1) 

        # Save the eroded image 
        cv.imwrite('./resultsMultiErosionKernel/kernel' + str(tailleKernel) + "_" + fileName + '/eroded' + str(i + 1) + '.png', eroded_image)
        
    # Close the file
    hdul.close()
    

if __name__ == "__main__": 
    #on fait 5 erosion et un kernel de 1 
    multiErosionKernel("./../examples/HorseHead.fits", 5, 1) 
    multiErosionKernel("./../examples/test_M31_linear.fits", 5, 1)
    multiErosionKernel("./../examples/test_M31_raw.fits", 5, 1)
    
    #on fait 5 erosion et un kernel de 10 
    multiErosionKernel("./../examples/HorseHead.fits", 5, 10) 
    multiErosionKernel("./../examples/test_M31_linear.fits", 5, 10)
    multiErosionKernel("./../examples/test_M31_raw.fits", 5, 10)
    