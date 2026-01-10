from reduce_stars import reduce_stars 
from saveImage import saveImage 

image = reduce_stars("./../examples/HorseHead.fits", fwhm=8.0, threshold=5.0, kernelSize=8, ksize=6, sigmaX=4) 
saveImage(image, "pornoAnnee50", "./") 