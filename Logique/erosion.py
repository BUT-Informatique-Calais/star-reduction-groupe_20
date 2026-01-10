from astropy.io import fits
import cv2 as cv
import numpy as np
from .saveImage import saveImage

def erosion(fitsFile: str, kernelSize: int = 3) -> np.ndarray:
    """Fonction qui fait de l'erosion sur un fichier .fits 
    
    Args:
        fitsFile (str): le chemin du fichier .fits
        kernelSize (int): la taille du noyau de l'erosion
    
    Returns:
        np.ndarray: l'image erosionnée
    """ 
    # Open and read the FITS file
    hdul = fits.open(fitsFile)

    # Access the data from the primary HDU
    data = hdul[0].data

    # Handle both monochrome and color images 
    if data.ndim == 3:
        # Color image - need to transpose to (height, width, channels)
        if data.shape[0] == 3:  # If channels are first: (3, height, width)
            data = np.transpose(data, (1, 2, 0))
        # If already (height, width, 3), no change needed
        
        # Normalize each channel separately to [0, 255] for OpenCV
        image = np.zeros_like(data, dtype='uint8')
        
        for i in range(data.shape[2]):
            channel = data[:, :, i]
            image[:, :, i] = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype('uint8')
            
        # Passage de RGB a BGR 
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    else:
        # Convert to uint8 for OpenCV
        image = ((data - data.min()) / (data.max() - data.min()) * 255).astype('uint8')

    # Define a kernel for erosion
    kernel = np.ones((kernelSize,kernelSize), np.uint8)
    
    # Perform erosion
    eroded_image = cv.erode(image, kernel, iterations=1) #image a la place de hdul[0].data 

    hdul.close()
    return eroded_image


if __name__ == "__main__": 
    print("----------TEST----------")
    saveImage(erosion("./../examples/HorseHead.fits"), "eroded", "results/HorseHead") 
    saveImage(erosion("./../examples/test_M31_linear.fits"), "eroded", "results/test_M31_linear")
    saveImage(erosion("./../examples/test_M31_raw.fits"), "eroded", "results/test_M31_raw") 