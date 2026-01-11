import numpy as np
import numpy.typing as npt
import cv2 as cv
from .saveImage import saveImage
from .masque import getMask

def getMaskSoft(mask: npt.NDArray[np.uint8], ksize: int = 3, sigmaX: float = 1.5) -> npt.NDArray[np.uint8]:
    """Effectue le flou gaussien sur un masque. 
    
    Args:
        mask (npt.NDArray[np.uint8]): Masque binaire.
        ksize (int): Taille du noyau du flou gaussien 
        sigmaX (float): Paramètre du flou gaussien 
    
    Returns:
        npt.NDArray[np.uint8]: Masque binaire adouci.
    """
    # ksize doit être impair. SigmaX=0 laisse cv calculer sigma
    if ksize % 2 == 0:
        ksize += 1

    return cv.GaussianBlur(mask, (ksize, ksize), sigmaX)


if __name__ == "__main__":
    print("----------TEST----------")
    saveImage(getMaskSoft(getMask("./../examples/HorseHead.fits")), "maskSoft", "results/HorseHead")
    saveImage(getMaskSoft(getMask("./../examples/test_M31_linear.fits")), "maskSoft", "results/test_M31_linear")
    saveImage(getMaskSoft(getMask("./../examples/test_M31_raw.fits")), "maskSoft", "results/test_M31_raw")
