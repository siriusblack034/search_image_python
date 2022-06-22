import numpy as np
import csv
from scipy.spatial import distance


class Distance:
    def __init__(self, indexPath):
        self.indexPath = indexPath

    def distanceShape(self, queryFeature):
        results = {}
        with open(self.indexPath) as f:
            reader = csv.reader(f)
            # color
            for row in reader:
                features = [float(x) for x in row[1:]]
                d = distance.euclidean(features, queryFeature)
                results[row[0]] = d
            f.close()
        return results

    def distanceColor(self, queryFeature):
        results = {}
        with open(self.indexPath) as f:
            reader = csv.reader(f)
            # color
            for row in reader:
                featuresCorner = [float(x) for x in row[1:1153]]
                featuresCornerQuery = [float(x) for x in queryFeature[0:1152]]
                distanceCorner = distance.euclidean(
                    featuresCorner, featuresCornerQuery)
                featuresCircle = [float(x) for x in row[1153:]]
                featuresCircleQuery = [float(x) for x in queryFeature[1152:]]
                distanceCircle = distance.euclidean(
                    featuresCircle, featuresCircleQuery)
                results[row[0]] = (distanceCorner + distanceCircle*2)/3
            f.close()
        return results
