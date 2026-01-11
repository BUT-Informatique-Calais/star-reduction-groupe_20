import os 
import numpy.typing as npt
import numpy as np
import cv2 as cv


def saveImage(image: npt.NDArray[np.uint8], fileName: str, folderDestination: str = "results")-> None:
    """Enregistrement de l'image dans folderDestination. (attention peut écraser une image) 
    
    Args:
        image (npt.NDArray[np.uint8]): l'image à enregistrer
        fileName (str): le nom du fichier
        folderDestination (str): dossier de destination
    """
    # création du dossier pour stockage des résultat : 
    os.makedirs(folderDestination, exist_ok=True)

    # Save the eroded image 
    cv.imwrite(folderDestination + '/' + fileName + '.png', image)


if __name__ == "__main__": 
    from .original import getOriginal
    from .erosion import erosion
    from .masque import getMask
    from .masqueSoft import getMaskSoft
    from .reduce_stars import reduce_stars
    
    print("---------TEST----------") 
    print("création de original, erosion, mask, maskSoft, final des .fits de ./../examples") 

    # original : 
    saveImage(getOriginal("./../examples/HorseHead.fits"), "original", "results/HorseHead") 
    saveImage(getOriginal("./../examples/test_M31_linear.fits"), "original", "results/test_M31_linear") 
    saveImage(getOriginal("./../examples/test_M31_raw.fits"), "original", "results/test_M31_raw") 

    # erosion : 
    saveImage(erosion("./../examples/HorseHead.fits"), "erosion", "results/HorseHead") 
    saveImage(erosion("./../examples/test_M31_linear.fits"), "erosion", "results/test_M31_linear") 
    saveImage(erosion("./../examples/test_M31_raw.fits"), "erosion", "results/test_M31_raw") 

    # mask : 
    saveImage(getMask("./../examples/HorseHead.fits"), "mask", "results/HorseHead") 
    saveImage(getMask("./../examples/test_M31_linear.fits"), "mask", "results/test_M31_linear") 
    saveImage(getMask("./../examples/test_M31_raw.fits"), "mask", "results/test_M31_raw") 

    # maskSoft : 
    saveImage(getMaskSoft(getMask("./../examples/HorseHead.fits")), "maskSoft", "results/HorseHead") 
    saveImage(getMaskSoft(getMask("./../examples/test_M31_linear.fits")), "maskSoft", "results/test_M31_linear") 
    saveImage(getMaskSoft(getMask("./../examples/test_M31_raw.fits")), "maskSoft", "results/test_M31_raw") 

    # final : 
    saveImage(reduce_stars("./../examples/HorseHead.fits"), "final", "results/HorseHead") 
    saveImage(reduce_stars("./../examples/test_M31_linear.fits"), "final", "results/test_M31_linear") 
    saveImage(reduce_stars("./../examples/test_M31_raw.fits"), "final", "results/test_M31_raw") 