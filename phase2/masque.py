from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from astropy.table import Table
import cv2 as cv
import numpy as np
import os
import numpy.typing as npt


def getMask(fitsFile: str, fwhm: float = 3.0, threshold: float = 1.0) -> npt.NDArray[np.uint8]:
    """Génère un masque binaire des étoiles en utilisant DAOStarFinder.
    
    Args:
        fitsFile (str): Chemin du fichier fits
        fwhm (float): Largeur à mi-hauteur de l'étoile 
        threshold (float): Le seuil de détection 
        
    Returns:
        mask (npt.NDArray[np.uint8]): Image binaire où les étoiles détectées sont marquées.
    """
    # Open and read the FITS file
    hdul: fits.HDUList = fits.open(fitsFile)
    
    # Access the data from the primary HDU
    data: np.ndarray = hdul[0].data
    
    # Handle both monochrome and color images
    if data.ndim == 3: 
        # Si (3, H, W) -> (H, W, 3)
        if data.shape[0] == 3:
            data = np.transpose(data, (1, 2, 0))
        
        gray_data: np.ndarray = np.mean(data, axis=2)
    else: 
        gray_data: np.ndarray = data


    # Estimation du bruit de fond
    mean: float
    median: float
    std: float
    mean, median, std = sigma_clipped_stats(gray_data, sigma=3.0)
    
    # Configuration de DAOStarFinder
    daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold * std) 
    
    # Détection des sources
    sources: Table | None = daofind(gray_data - median) 
    
    # Création du masque vide (noir) typé explicitement en uint8
    mask: npt.NDArray[np.uint8] = np.zeros_like(gray_data, dtype=np.uint8)
    
    # Si pas d'étoiles détectées
    if sources is None:
        print("Aucune étoile détectée.")
        return mask
    
    # Récupération des positions.
    # On stack x et y pour obtenir un tableau (N, 2)
    positions: npt.NDArray[np.float64] = np.transpose((sources['xcentroid'], sources['ycentroid']))
    
    # Rayon des cercles à dessiner
    radius: int = int(max(1, fwhm * 1.5 / 2))
    
    for pos in positions:
        # OpenCv utilise (x, y) en entiers
        center = (int(round(pos[0])), int(round(pos[1])))
        
        # Couleur 255 (blanc), épaisseur -1 (rempli)
        cv.circle(mask, center, radius, 255, thickness=-1)
    
    hdul.close()
        
    # print(f"Nombre d'étoiles détectées : {len(sources)}")
    return mask


def saveMasque(fitsFile: str, mask: npt.NDArray[np.uint8]) -> None:
    """Traitement d'un fichier fits
    
    Args:
        fitsFile: Chemin du fichier fits
        mask: masque binaire 
    """
    # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
    fileName: str = fitsFile.split("/")[-1].removesuffix(".fits") 

    # création du dossier pour stockage des résultat : 
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/" + fileName, exist_ok=True)

    cv.imwrite("results/" + fileName + "/mask.png", mask)

if __name__ == "__main__":
    saveMasque("./../examples/HorseHead.fits", getMask("./../examples/HorseHead.fits")) 
    saveMasque("./../examples/test_M31_linear.fits", getMask("./../examples/test_M31_linear.fits"))
    saveMasque("./../examples/test_M31_raw.fits", getMask("./../examples/test_M31_raw.fits"))
    
