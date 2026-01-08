from astropy.io import fits
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
from masque import getMask #voir masque.py
# Ajout du dossier parent (..) au path pour importer erosion.py
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from erosion import erosion #voir erosion.py


def reduce_stars(fitsFile: str, fwhm: float = 3.0, threshold: float = 1.0, kernelSize: int = 3, ksize: int = 3, sigmaX: float = 1.5) -> list[dict]:
    """
    Réduit l'intensité des étoiles dans une image FITS en utilisant un masque.
    
    Logique:
    1. Créer une version érodée de l'image (I_erode).
    2. Créer un masque d'étoiles (M) et l'adoucir (flou gaussien).
    3. Calculer l'image finale : I_final = (M * I_erode) + ((1 - M) * I_original).

    Args:
        fitsFile (str): Chemin du fichier FITS à traiter.
        fwhm (float): Largeur à mi-hauteur de l'étoile PARAMETRE A AJUSTER DANS LA VUE 
        threshold (float): Le seuil de détection PARAMETRE A AJUSTER DANS LA VUE
        kernelSize (int): Taille du noyau de l'érosion PARAMETRE A AJUSTER DANS LA VUE
        ksize (int): Taille du noyau du flou gaussien PARAMETRE A AJUSTER DANS LA VUE
        sigmaX (float): Paramètre du flou gaussien PARAMETRE A AJUSTER DANS LA VUE
    
    Returns:
        list (list[dict]): Une liste de dictionnaires contenant les informations des images à sauvegarder. (original.png / eroded.png / masque.png / masqueSoft.png / final.png)
              Format: [{'path': str, 'data': numpy array, 'method': 'plt'|'cv'}]
    """
    print(f"Traitement du fichier : {fitsFile}")
    
    # Lecture du fichier FITS
    hdul: fits.HDUList = fits.open(fitsFile)

    data: np.ndarray = hdul[0].data

    # Gestion des dimensions (couleur vs monochrome)
    if data.ndim == 3: #si couleur 
        # Si (3, H, W) -> (H, W, 3)
        if data.shape[0] == 3:
            data = np.transpose(data, (1, 2, 0))

    # else: #si monochrome
    #     pass


    #####################################
    # Etape 1 : Version érodée (Ierode) #
    #####################################

    i_erode = erosion(fitsFile, kernelSize)


    ##############################
    # Etape 2 : Masque d'étoiles #
    ##############################
    
    masque = getMask(fitsFile, fwhm, threshold) 

    # Adoucir les bords (Flou Gaussien)
    # ksize doit être impair. SigmaX=0 laisse cv calculer sigma
    if ksize % 2 == 0:
        ksize += 1

    masqueSoft = cv.GaussianBlur(masque, (ksize, ksize), sigmaX)


    ####################################
    # Etape 3 : Interpolation (Ifinal) #
    ####################################
    
    # formule : Ifinal = (M ×Ierode)+((1−M )×Ioriginal)
    
    # 1. Normalisation du masque [0, 255] -> [0, 1]
    M = masqueSoft.astype(np.float32) / 255.0
    
    # 2. Gestion des dimensions du masque pour le broadcasting sur image couleur (H, W, 1)
    if data.ndim == 3 and M.ndim == 2:
        M = M[..., np.newaxis]
    
    # 3. Preparation des images
    # data est lu via astropy, peut être n'importe quoi (float, int), range arbitraire.
    # i_erode est uint8 [0-255], BGR (OpenCV).

    # Normalisation de data vers [0, 255] pour matcher i_erode
    data_float = data.astype(np.float32)
    data_norm = cv.normalize(data_float, None, 0, 255, cv.NORM_MINMAX)

    # Conversion de i_erode (BGR) vers RGB pour matcher data (qui est RGB)
    i_erode_rgb = i_erode.astype(np.float32)
    if i_erode.ndim == 3:
        i_erode_rgb = cv.cvtColor(i_erode, cv.COLOR_BGR2RGB).astype(np.float32)
    
    # Si image n&b, i_erode pourrait être couleur ou n&b selon erosion.py
    # Si i_erode est 3D et data_norm est 2D, il faut adapter
    if data_norm.ndim == 2 and i_erode_rgb.ndim == 3:
        i_erode_rgb = cv.cvtColor(i_erode, cv.COLOR_BGR2GRAY).astype(np.float32)

    # 4. Calcul final
    i_final = (M * i_erode_rgb) + ((1.0 - M) * data_norm)


    ############################
    # Etape 4 : enregistrement #
    ############################

    # Préparation de la liste des fichiers
    fileName = fitsFile.split("/")[-1].removesuffix(".fits")
    resultFiles = []

    # original.png
    resultFiles.append({
        'path': f"./results/{fileName}/original.png",
        'data': data,
        'method': 'plt'
    })

    # eroded.png
    resultFiles.append({
        'path': f"./results/{fileName}/eroded.png",
        'data': i_erode,
        'method': 'cv'
    })
    
    # masque.png
    resultFiles.append({
        'path': f"./results/{fileName}/masque.png",
        'data': masque,
        'method': 'cv'
    })
    
    # masqueSoft.png
    resultFiles.append({
        'path': f"./results/{fileName}/masqueSoft.png",
        'data': masqueSoft,
        'method': 'cv'
    })

    # final.png
    resultFiles.append({
        'path': f"./results/{fileName}/final.png",
        'data': i_final, # Sera traité (transposé/normalisé) par saveImage si besoin
        'method': 'plt'
    })

    hdul.close()
    print(f"Terminé pour {fileName}")
    
    return resultFiles


def saveImage(img_list: list[dict]) -> None:
    """Enregistre les images fournies dans la liste. Gère les spécificités de plt.imsave (normalisation) et cv.imwrite.
    
    Args:
        img_list (list[dict]): Liste des images à enregistrer (normalement : (original.png / eroded.png / masque.png / masqueSoft.png / final.png))
    """
    for item in img_list:
        path = item['path']
        data = item['data']
        method = item['method'] # 'plt' ou 'cv'
        
        # Création du dossier parent si nécessaire
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        if method == 'cv':
            cv.imwrite(path, data)
             
        elif method == 'plt':
            # Logique de sauvegarde avec Matplotlib (reprise du code original)
            
            # Handle both monochrome and color images 
            if data.ndim == 3:
                # Si (3, H, W) -> (H, W, 3)
                if data.shape[0] == 3:
                    data = np.transpose(data, (1, 2, 0))
                
                # Normalisation [0, 1] pour éviter les avertissements/erreurs matplotlib avec des floats hors range
                # Le code original normalisait systématiquement les images couleurs
                if data.max() != data.min(): # Eviter division par zero
                    data = (data - data.min()) / (data.max() - data.min())
                else:
                    data = np.zeros_like(data) # Ou autre gestion par défaut
                
                plt.imsave(path, data)
                
            else:
                # Image Monochrome
                plt.imsave(path, data, cmap='gray')


if __name__ == "__main__":
    # paramètre a adaptée pour chaque image : par défaut mettre par défaut 
    images = reduce_stars("./../examples/HorseHead.fits", fwhm=3.0, threshold=2.0, kernelSize=3, ksize=3, sigmaX=1.5) 
    saveImage(images)
    
    images = reduce_stars("./../examples/test_M31_linear.fits", fwhm=3.0, threshold=5.0, kernelSize=3, ksize=3, sigmaX=1.5) 
    saveImage(images)
    
    images = reduce_stars("./../examples/test_M31_raw.fits")
    saveImage(images)