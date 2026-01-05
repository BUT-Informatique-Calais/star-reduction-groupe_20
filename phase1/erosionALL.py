#############################
# erosion pour chaque .fits #
#############################

from astropy.io import fits
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import os

def erosion(fitsFile: str)->None :
    """fonction qui fait de l'erosion sur un fichier .fits 
    
    Args:
        fitsFile (str): le chemin du fichier .fits
    """ 
    # Open and read the FITS file
    hdul = fits.open(fitsFile)
    
    # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
    fileName = fitsFile.split("/")[-1].removesuffix(".fits") 
    
    # création du dossier pour stockage des résultat : 
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/" + fileName, exist_ok=True)
    

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
        plt.imsave('./results/' + fileName + '/original.png', data_normalized)
        
        # Normalize each channel separately to [0, 255] for OpenCV
        image = np.zeros_like(data, dtype='uint8')
        
        for i in range(data.shape[2]):
            channel = data[:, :, i]
            image[:, :, i] = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype('uint8')
            
        # Passage de RGB a BGR 
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    else:
        # Monochrome image
        plt.imsave('./results/' + fileName + '/original.png', data, cmap='gray')
        
        # Convert to uint8 for OpenCV
        image = ((data - data.min()) / (data.max() - data.min()) * 255).astype('uint8')



    # Define a kernel for erosion
    kernel = np.ones((3,3), np.uint8)
    # Perform erosion
    eroded_image = cv.erode(image, kernel, iterations=1)

    # Save the eroded image 
    cv.imwrite('./results/' + fileName + '/eroded.png', eroded_image)

    # Close the file
    hdul.close()
    
    
    
if __name__ == "__main__": 
    erosion("./../examples/HorseHead.fits") 
    erosion("./../examples/test_M31_linear.fits")
    erosion("./../examples/test_M31_raw.fits") 