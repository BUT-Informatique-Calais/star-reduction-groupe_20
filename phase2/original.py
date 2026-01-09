from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from astropy.table import Table
import cv2 as cv
import numpy as np
import os
import numpy.typing as npt
import matplotlib.pyplot as plt

def getOriginal(fitsFile: str) -> npt.NDArray[np.uint8]:
    """Génère l'image originale 
    
    Args:
        fitsFile (str): Chemin du fichier fits
    
    Returns:
        original (npt.NDArray[np.uint8]): Image originale 
    """
    # Lecture du fichier FITS
    hdul: fits.HDUList = fits.open(fitsFile)

    data: np.ndarray = hdul[0].data

    # Gestion des dimensions (couleur vs monochrome)
    if data.ndim == 3: #si couleur 
        # Si (3, H, W) -> (H, W, 3)
        if data.shape[0] == 3:
            data = np.transpose(data, (1, 2, 0))
        
        # Normalisation [0, 1] pour éviter les avertissements/erreurs matplotlib avec des floats hors range
        # Le code original normalisait systématiquement les images couleurs
        if data.max() != data.min(): # Eviter division par zero
            data = (data - data.min()) / (data.max() - data.min())
        else:
            data = np.zeros_like(data) # Ou autre gestion par défaut
        
    # monochorme ne rien faire 

    return data


def saveOriginal(fitsFile: str, original: npt.NDArray[np.uint8]) -> None:
    """Traitement d'un fichier fits
    
    Args:
        fitsFile: Chemin du fichier fits
        original: image originale 
    """
    # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
    fileName: str = fitsFile.split("/")[-1].removesuffix(".fits") 

    # création du dossier pour stockage des résultat : 
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/" + fileName, exist_ok=True)

    if original.ndim == 3:
        plt.imsave("results/" + fileName + "/original.png", original)
    
    else: 
        plt.imsave("results/" + fileName + "/original.png", original, cmap='gray')
        

if __name__ == "__main__":
    saveOriginal("./../examples/HorseHead.fits", getOriginal("./../examples/HorseHead.fits")) 
    saveOriginal("./../examples/test_M31_linear.fits", getOriginal("./../examples/test_M31_linear.fits"))
    saveOriginal("./../examples/test_M31_raw.fits", getOriginal("./../examples/test_M31_raw.fits"))
    
