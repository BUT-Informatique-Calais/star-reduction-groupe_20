from astropy.io import fits
import cv2 as cv
import numpy as np
import numpy.typing as npt
from saveImage import saveImage 

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
        if data.max() != data.min(): # Eviter division par zero
            data = (data - data.min()) / (data.max() - data.min())
        else:
            data = np.zeros_like(data) 
            
        # Conversion uint8 et passage en BGR pour OpenCV
        data = (data * 255).astype(np.uint8)
        original = cv.cvtColor(data, cv.COLOR_RGB2BGR)
        
    else:
        # Monochrome : Normalisation et conversion uint8
        if data.max() != data.min():
            data = (data - data.min()) / (data.max() - data.min())
        else:
            data = np.zeros_like(data)

        original = (data * 255).astype(np.uint8)
    
    hdul.close()
    return original
        

if __name__ == "__main__":
    print("----------TEST----------")
    saveImage(getOriginal("./../examples/HorseHead.fits"), "original", "results/HorseHead") 
    saveImage(getOriginal("./../examples/test_M31_linear.fits"), "original", "results/test_M31_linear")
    saveImage(getOriginal("./../examples/test_M31_raw.fits"), "original", "results/test_M31_raw")