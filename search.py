# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.distance import Distance
import argparse
import cv2

from pyimagesearch.shapedescriptor import ShapeDescriptor


class Search:
    def __init__(self, imagePath):
        self.imagePath = imagePath

    def searching(self):
        cd = ColorDescriptor((8, 12, 3))
        sd = ShapeDescriptor(9)
        query = cv2.imread(self.imagePath)
        query = cv2.resize(src=query,  dsize=(800, 800))
        featuresColor = cd.describe(query)
        featuresShape = sd.describe(self.imagePath)
        searcherColor = Distance("color.csv")
        searcherShape = Distance("shape.csv")
        resultsColor = searcherColor.distanceColor(featuresColor)
        resultShape = searcherShape.distanceShape(featuresShape)

        results = {}
        for attr, value in resultsColor.items():
            distanceColor = resultsColor[attr]
            distanceShape = resultShape[attr]
            print(attr)
            print("     distanceColor:" + str(distanceColor))
            print("     distanceShape:" + str(distanceShape))
            results[attr] = float((distanceColor*5 + distanceShape)/6)
            print("     results:" + str(results[attr]))
        results = sorted([(v, k) for (k, v) in results.items()])
        return results[:10]
