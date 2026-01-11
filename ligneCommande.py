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

                if fwhm <= 0:
                    raise ValueError # = allez au except ValueError

            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -fwhm doit être un nombre strictement positif (float). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-threshold=" in sys.argv[i]: 
            try:
                threshold = float(sys.argv[i].split("=")[1])

                if threshold <= 0:
                    raise ValueError

            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -threshold doit être un nombre strictement positif (float). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-kernelSize=" in sys.argv[i]: 
            try:
                kernelSize = int(sys.argv[i].split("=")[1])

                if kernelSize <= 0:
                    raise ValueError

            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -kernelSize doit être un entier strictement positif (int). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-ksize=" in sys.argv[i]: 
            try:
                ksize = int(sys.argv[i].split("=")[1])

                if ksize <= 0:
                    raise ValueError

            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -ksize doit être un entier strictement positif (int). Valeur reçue : {sys.argv[i].split('=')[1]}")

        elif "-sigmaX=" in sys.argv[i]: 
            try:
                sigmaX = float(sys.argv[i].split("=")[1])

                if sigmaX <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError(f"ERREUR : La valeur de -sigmaX doit être un nombre strictement positif (float). Valeur reçue : {sys.argv[i].split('=')[1]}")
        
        else: 
            raise ValueError(f"ERREUR : Argument \"{sys.argv[i]}\" inconnue. Usage: python ligneCommande.py <fitsFolder> [-folderDestination=...] [-fwhm=...] [-threshold=...] [-kernelSize=...] [-ksize=...] [-sigmaX=...]")
        
        i += 1

    return fitsFolder, folderDestination, fwhm, threshold, kernelSize, ksize, sigmaX


def chargementParametresInteractif() -> tuple[str, str, float, float, int, int, float]:
    """Fonction qui charge les paramètres interactivement.

    Returns:
        tuple[str, str, float, float, int, int, float]: Un tuple contenant les paramètres chargés.
    """
    buffer: str = ""

    # valeur par défaut : 
    folderDestination: str = "./results"
    fwhm: float = 3.0
    threshold: float = 1.0
    kernelSize: int = 3
    ksize: int = 3
    sigmaX: float = 1.5


    fitsFolder = input("Entrez le chemin du dossier source [obligatoire] : ")
    verifieFitsFolder(fitsFolder) #fonction de vérification 

    buffer = input("Entrez le chemin du dossier de destination (par defaut : ./results) : ") 
    if buffer != "" : folderDestination = buffer # else : valeur par défaut qui est déja initialisée
    
    try:
        buffer = input("Entrez la valeur de fwhm (par defaut : 3.0) : ")
        if buffer != "" : fwhm = float(buffer) # else : valeur par défaut qui est déja initialisée

        if fwhm <= 0:
            raise ValueError # = allez au except ValueError

    except ValueError:
        raise ValueError(f"ERREUR : La valeur de fwhm doit être un nombre strictement positif (float). Valeur reçue : \"{buffer}\"")

    try:
        buffer = input("Entrez la valeur de threshold (par defaut : 1.0) : ")
        if buffer != "" : threshold = float(buffer)

        if threshold <= 0:
            raise ValueError

    except ValueError:
        raise ValueError(f"ERREUR : La valeur de threshold doit être un nombre strictement positif (float). Valeur reçue : \"{buffer}\"")

    try:
        buffer = input("Entrez la valeur de kernelSize (par defaut : 3) : ")
        if buffer != "" : kernelSize = int(buffer)

        if kernelSize <= 0:
            raise ValueError

    except ValueError:
        raise ValueError(f"ERREUR : La valeur de kernelSize doit être un entier strictement positif (int). Valeur reçue : \"{buffer}\"")

    try:
        buffer = input("Entrez la valeur de ksize (par defaut : 3) : ")
        if buffer != "" : ksize = int(buffer)

        if ksize <= 0:
            raise ValueError

    except ValueError:
        raise ValueError(f"ERREUR : La valeur de ksize doit être un entier strictement positif (int). Valeur reçue : \"{buffer}\"")

    try:
        buffer = input("Entrez la valeur de sigmaX (par defaut : 1.5) : ")
        if buffer != "" : sigmaX = float(buffer)

        if sigmaX <= 0:
            raise ValueError

    except ValueError:
        raise ValueError(f"ERREUR : La valeur de sigmaX doit être un nombre strictement positif (float). Valeur reçue : \"{buffer}\"")
    

    return fitsFolder, folderDestination, fwhm, threshold, kernelSize, ksize, sigmaX


def mainBash(interaction: bool = False) -> None:
    """Fonction principale qui s'occupe de tout le traitement des fichiers. 

    Args:
        interaction (bool, optional): Si True, le programme demande les paramètres interactivement. Par défaut, False.
    

    Exemple de lancement avec interraction : 
    -> ligneCommande.py

    Exemple de lancement sans interraction : 
    -> ligneCommande.py ./examples -folderDestination=./results -fwhm=3 -threshold=1 -kernelSize=3 -ksize=3 -sigmaX=1.5

    REMARQUE : Les arguments peuvent être placer dans n'importe quel ordre sauf le premier 
               Tout les arguments sont optionnel sauf le premier 
               L'argument fitsFolder et folderDestination peuve s'écrire "./exemple" ou "exemple" (le "./" n'est pas nécessaire)
    """
    # affichage du logo : 
    print("                               ..                 ___ _                         \n                             .. .                / __| |_ __ _ _ _ ___          \n                .-==++++++++.   ..               \\__ \\  _/ _` | '_(_-<          \n             .=======++++++++++- .=+###*=:.       |___/\\__\\__,_|_| /__/          \n           .===========+++++++++++  -#######-     | _ \\___ __| |_  _ __ ___ _ _  \n          ==============+++++++++++  *#######     |   / -_) _` | || / _/ -_) '_| \n         =================+++++++++ .#######*     |_|_\\___\\__,_|\\_,_\\__\\___|_|   \n        ===================+++++++..#######*     \n       .=====================+++: ########:      \n       :======================..########=       \n     . :===================:.*########-         \n   +#  .------=========: -#########*+=          \n .###*   .-------:. .+###########+=++.          \n:########*+==**##############+======.           \n#########################+---------.            \n#####################-------------              \n .############+----------------:                \n                .:----------.                   \n\n")

    # chargement des arguments : 
    if interaction == False: 
        # utilisation de chargementArgument()
        fitsFolder, folderDestination, fwhm, threshold, kernelSize, ksize, sigmaX = chargementArgument() 
    else: 
        # utilisation de chargementParametresInteractif()
        fitsFolder, folderDestination, fwhm, threshold, kernelSize, ksize, sigmaX = chargementParametresInteractif() 

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


def bashInterface() -> None: 
    """Fonction qui lance mainBash(interaction=True) en boucle infinie avec gestion des erreurs. """
    while True : 
        try: 
            mainBash(interaction=True) 
            print("Appuilez sur une touche pour redémarer")
            input()
            os.system('cls' if os.name == 'nt' else 'clear') #clear du terminal
        except ValueError as erreurMessage: 
            print(erreurMessage)
            print("Appuilez sur une touche pour redémarer")
            input()
            os.system('cls' if os.name == 'nt' else 'clear') #clear du terminal



if __name__ == "__main__": 
    if len(sys.argv) > 1 : # si on a 1 argument : 
        mainBash(interaction=False) # sans interaction
    else: # sinon avec interaction :  
        bashInterface()