from astropy.io import fits
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import os 

def erosion(fitsFile: str, kernelSize: int = 3) -> np.ndarray:
    """fonction qui fait de l'erosion sur un fichier .fits 
    
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

    # Close the file
    hdul.close()
    
    return eroded_image


def saveErosion(fitsFile: str, erosion_image: np.ndarray) -> None:
    """
    Enregistre l'image erosionnée dans un dossier spécifique.
    
    Args:
        fitsFile (str): le chemin du fichier .fits
        erosion_image (np.ndarray): l'image erosionnée
    """
    # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
    fileName = fitsFile.split("/")[-1].removesuffix(".fits") 
    
    # création du dossier pour stockage des résultat : 
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/" + fileName, exist_ok=True)

    # Save the eroded image 
    cv.imwrite('./results/' + fileName + '/eroded.png', erosion_image)


if __name__ == "__main__": 
    saveErosion("./examples/HorseHead.fits", erosion("./examples/HorseHead.fits")) 
    saveErosion("./examples/test_M31_linear.fits", erosion("./examples/test_M31_linear.fits"))
    saveErosion("./examples/test_M31_raw.fits", erosion("./examples/test_M31_raw.fits")) 