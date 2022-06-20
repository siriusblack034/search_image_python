# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
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
        featuresColor = cd.describe(query)
        featuresShape = sd.describe(self.imagePath)
        searcherColor = Searcher("color.csv")
        searcherShape = Searcher("shape.csv")
        resultsColor = searcherColor.distanceColor(featuresColor)
        resultShape = searcherShape.distanceShape(featuresShape)
        """ f = open("demofile2.txt", "a")
        featuresShape = [str(f) for f in featuresShape]
        f.write(str(featuresShape))
        f.close() """
        results = {}
        for attr, value in resultsColor.items():
            distanceColor = resultsColor[attr]
            distanceShape = resultShape[attr]
            print(attr)
            print("     distanceColor:" + str(distanceColor))
            print("     distanceShape:" + str(distanceShape))
            results[attr] = float((distanceColor*4 + distanceShape)/5)
            print("     results:" + str(results[attr]))

        results = sorted([(v, k) for (k, v) in results.items()])
        return results[:10]
