import sys
import os
from reduce_stars import reduce_stars 
from saveImage import saveImage 

def verifieFitsFolder(fitsFolder: str) -> None: 
    """Fonction qui vérifie si le dossier fitsFolder existe et contient des fichiers fits.

    Args:
        fitsFolder (str): Le dossier contenant les fichiers fits.
    """
    if not os.path.exists(fitsFolder): 
        raise ValueError(f"ERREUR : Le dossier fitsFolder \"{fitsFolder}\" n'existe pas.")
    
    if not any(fitsFolder.endswith(".fits") for fitsFolder in os.listdir(fitsFolder)): 
        raise ValueError(f"ERREUR : Le dossier fitsFolder \"{fitsFolder}\" ne contient pas de fichiers fits.")


def chargementArgument() -> tuple[str, str, float, float, int, int, float]:
    """Fonction qui charge les arguments passés en ligne de commande.

    Returns:
        tuple[str, str, float, float, int, int, float]: Un tuple contenant les arguments chargés.
    """
    # pour fitsFolder : 
    if len(sys.argv) > 1: #argument obligatoire 
        verifieFitsFolder(sys.argv[1]) # on vérifie que le dossier existe et contient des fichiers fits. 
        fitsFolder = sys.argv[1]
    else: 
        raise ValueError("ERREUR : L'argument fitsFolder est manquant. Usage: python ligneCommande.py <fitsFolder> [-folderDestination=...] [-fwhm=...] [-threshold=...] [-kernelSize=...] [-ksize=...] [-sigmaX=...]")

    # valeur par défaut : 
    folderDestination: str = "./results"
    fwhm: float = 3.0
    threshold: float = 1.0
    kernelSize: int = 3
    ksize: int = 3
    sigmaX: float = 1.5

    # on regarde les paramètre passés en ligne de commande
    i = 2 # (on passe le premier argument) 
    while i < len(sys.argv): 
        if "-folderDestination=" in sys.argv[i]: 
            folderDestination = sys.argv[i].split("=")[1] # REMARQUE : on ne vérifie pas si le dossier existe car si il n'existe pas on le crée. 

        elif "-fwhm=" in sys.argv[i]: 
            try:
                fwhm = float(sys.argv[i].split("=")[1])
            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -fwhm doit être un nombre (float). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-threshold=" in sys.argv[i]: 
            try:
                threshold = float(sys.argv[i].split("=")[1])
            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -threshold doit être un nombre (float). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-kernelSize=" in sys.argv[i]: 
            try:
                kernelSize = int(sys.argv[i].split("=")[1])
            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -kernelSize doit être un entier (int). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-ksize=" in sys.argv[i]: 
            try:
                ksize = int(sys.argv[i].split("=")[1])
            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -ksize doit être un entier (int). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-sigmaX=" in sys.argv[i]: 
            try:
                sigmaX = float(sys.argv[i].split("=")[1])
            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -sigmaX doit être un nombre (float). Valeur reçue : {sys.argv[i].split('=')[1]}")
        
        else: 
            raise ValueError(f"ERREUR : Argument \"{sys.argv[i]}\" inconnue. Usage: python ligneCommande.py <fitsFolder> [-folderDestination=...] [-fwhm=...] [-threshold=...] [-kernelSize=...] [-ksize=...] [-sigmaX=...]")
        
        i += 1

    return fitsFolder, folderDestination, fwhm, threshold, kernelSize, ksize, sigmaX


if __name__ == "__main__": 
    print("                               ..                 ___ _                         \n                             .. .                / __| |_ __ _ _ _ ___          \n                .-==++++++++.   ..               \\__ \\  _/ _` | '_(_-<          \n             .=======++++++++++- .=+###*=:.       |___/\\__\\__,_|_| /__/          \n           .===========+++++++++++  -#######-     | _ \\___ __| |_  _ __ ___ _ _  \n          ==============+++++++++++  *#######     |   / -_) _` | || / _/ -_) '_| \n         =================+++++++++ .#######*     |_|_\\___\\__,_|\\_,_\\__\\___|_|   \n        ===================+++++++..#######*     \n       .=====================+++: ########:      \n       :======================..########=       \n     . :===================:.*########-         \n   +#  .------=========: -#########*+=          \n .###*   .-------:. .+###########+=++.          \n:########*+==**##############+======.           \n#########################+---------.            \n#####################-------------              \n .############+----------------:                \n                .:----------.                   \n\n")


    fitsFolder, folderDestination, fwhm, threshold, kernelSize, ksize, sigmaX = chargementArgument() 

    print("\n\n") 
    print("Chargement...\n") 

    # création si nécéssaire du dossier de destination : 
    os.makedirs(folderDestination, exist_ok=True) 

    # traitement de tout les .fits + enregistrement : 
    for file in os.listdir(fitsFolder): 
        if file.endswith(".fits"): 
            fitsFile = os.path.join(fitsFolder, file) 
            
            # Récupération du nom du fichier : le dernier "/" + retirer le ".fits" 
            fileName: str = fitsFile.split("/")[-1].removesuffix(".fits")
            fileName += "_star_reduced" 
            
            saveImage(reduce_stars(fitsFile, fwhm, threshold, kernelSize, ksize, sigmaX), fileName, folderDestination)

            print(f"{fitsFile} traité et enregistrer dans {folderDestination}") 

    
    print("Traitement terminé") 
