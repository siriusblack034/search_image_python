# import the necessary packages
from ast import arg
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.shapedescriptor import ShapeDescriptor
import argparse
import glob
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="Path to where the computed index will be stored")
ap.add_argument("-ic", "--index-color", required=True,
                help="Path to the result path description color")
ap.add_argument("-is", "--index-shape", required=True,
                help="Path to the result path description shape")
args = vars(ap.parse_args())
# initialize the color descriptor
HUE_BINS = 8
SATURATION_BINS = 12
VALUE_BINS = 3
cd = ColorDescriptor((HUE_BINS, SATURATION_BINS, VALUE_BINS))
ORIENTATIONS = 9
PIXELS_PER_CELL = (10, 10)
CELLS_PER_BLOCK = (2, 2)
TRANSFORM_SQRT = True
BLOCK_NORM = "L1"

sd = ShapeDescriptor(9)
# open the output index file for writing
outputColor = open(args["index_color"], "w")
outputShape = open(args["index_shape"], "w")
# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.png"):
    # extract the image ID (i.e. the unique filename) from the image
    # path and load the image itself
    imageID = imagePath[imagePath.rfind("\\") + 1:]
    image = cv2.imread(imagePath)
    # describe the image
    featuresColor = cd.describe(image)
    featuresColor = [str(f) for f in featuresColor]
    outputColor.write("%s,%s\n" % (imageID, ",".join(featuresColor)))
    imageGray = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    imageGray = cv2.resize(src=imageGray, dsize=(64, 128))
    # write the features to file
    featureShape = sd.describe("./"+imagePath)
    featureShape = [str(f) for f in featureShape]
    outputShape.write("%s,%s\n" % (imageID, ",".join(featureShape)))

# close the index file
outputColor.close()
outputShape.close()
