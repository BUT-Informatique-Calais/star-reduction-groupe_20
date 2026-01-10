from astropy.io import fits
import numpy as np
import numpy.typing as npt
from original import getOriginal 
from erosion import erosion 
from masque import getMask 
from masqueSoft import getMaskSoft 
from saveImage import saveImage 


def reduce_stars(fitsFile: str, fwhm: float = 3.0, threshold: float = 1.0, kernelSize: int = 3, ksize: int = 3, sigmaX: float = 1.5) -> npt.NDArray[np.uint8]:
    """
    Réduit l'intensité des étoiles dans une image FITS en utilisant un masque. (formule : Ifinal = (M *Ierode)+((1-M)*Ioriginal))

    Args:
        fitsFile (str): Chemin du fichier FITS à traiter.
        fwhm (float): Largeur à mi-hauteur de l'étoile  
        threshold (float): Le seuil de détection 
        kernelSize (int): Taille du noyau de l'érosion 
        ksize (int): Taille du noyau du flou gaussien 
        sigmaX (float): Paramètre du flou gaussien 
    
    Returns:
        npt.NDArray[np.uint8]: L'image finale après réduction des étoiles.
    """
    # print(f"Traitement du fichier : {fitsFile}")

    i_original = getOriginal(fitsFile)

    i_erode = erosion(fitsFile, kernelSize)
    
    masque = getMask(fitsFile, fwhm, threshold) 

    masqueSoft = getMaskSoft(masque, ksize, sigmaX)
    
    # formule : Ifinal = (M ×Ierode)+((1−M )×Ioriginal)

    # Normalisation du masque [0, 255] -> [0, 1]
    M = masqueSoft.astype(np.float32) / 255.0
    
    # Gestion des dimensions du masque pour le broadcasting sur image couleur (H, W, 1)
    if i_original.ndim == 3 and M.ndim == 2:
        M = M[..., np.newaxis]
    
    i_final = (M * i_erode) + ((1.0 - M) * i_original)
    i_final = i_final.astype(np.uint8) # Conversion en uint8 pour l'enregistrement avec OpenCV

    return i_final


if __name__ == "__main__":
    print("----------TEST----------")

    # paramètre a adaptée pour chaque image : par défaut mettre par défaut 
    saveImage(reduce_stars("./../examples/HorseHead.fits", fwhm=3.0, threshold=2.0, kernelSize=3, ksize=3, sigmaX=1.5), "final", "results/HorseHead") 
    saveImage(reduce_stars("./../examples/test_M31_linear.fits", fwhm=3.0, threshold=5.0, kernelSize=3, ksize=3, sigmaX=1.5), "final", "results/test_M31_linear") 
    saveImage(reduce_stars("./../examples/test_M31_raw.fits"), "final", "results/test_M31_raw")