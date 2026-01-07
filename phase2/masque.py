from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from astropy.table import Table
import cv2 as cv
import numpy as np
import os
import numpy.typing as npt


def getMask(imageData: npt.NDArray[np.floating], fwhm: float = 3.0, threshold: float = 1.0) -> npt.NDArray[np.uint8]:
    """
    Génère un masque binaire des étoiles en utilisant DAOStarFinder.
    
    Args:
        imageData: Données de l'image
        fwhm: Largeur à mi-hauteur de l'étoile 
        threshold: Le seuil de détection 
        
    Returns:
        mask: Image binaire où les étoiles détectées sont marquées.
    """
    # Estimation du bruit de fond
    mean: float
    median: float
    std: float
    mean, median, std = sigma_clipped_stats(imageData, sigma=3.0)
    
    # Configuration de DAOStarFinder
    daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold * std) 
    
    # Détection des sources
    sources: Table | None = daofind(imageData - median) 
    
    # Création du masque vide (noir) typé explicitement en uint8
    mask: npt.NDArray[np.uint8] = np.zeros_like(imageData, dtype=np.uint8)
    
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
        
    print(f"Nombre d'étoiles détectées : {len(sources)}")
    return mask


def processFitsFile(fitsFile: str, fwhm: float = 3, threshold: float = 1) -> None:
    """Traitement d'un fichier fits
    
    Args:
        fitsFile: Chemin du fichier fits
        fwhm: largeur de l'étoile
        threshold: seuil de détection

    REMARQUE : il seurai bien de pouvoir ajuster fwhm et threshold dans l'interface !!! 
    """
    # print(f"Traitement du fichier : {fitsFile}")
    hdul: fits.HDUList = fits.open(fitsFile)
    
    data: np.ndarray = hdul[0].data
    
    # Gestion des dimensions (couleur vs monochrome)
    if data.ndim == 3: #si couleur 
        # Si (3, H, W) -> (H, W, 3)
        if data.shape[0] == 3:
            data = np.transpose(data, (1, 2, 0))
        
        gray_data: np.ndarray = np.mean(data, axis=2)
    else: #si monochrome
        gray_data: np.ndarray = data


    # Création du masque avec DAOStarFinder
    mask: np.ndarray = getMask(gray_data, fwhm, threshold) 

    # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
    fileName: str = fitsFile.split("/")[-1].removesuffix(".fits") 

    # création du dossier pour stockage des résultat : 
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/" + fileName, exist_ok=True)

    cv.imwrite("results/" + fileName + "/mask.png", mask)
    hdul.close()

if __name__ == "__main__":
    processFitsFile("./../examples/HorseHead.fits") 
    processFitsFile("./../examples/test_M31_linear.fits")
    processFitsFile("./../examples/test_M31_raw.fits")
    
