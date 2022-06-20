import numpy as np
import csv
from scipy.spatial import distance


class Searcher:
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
                featuresCorner = [float(x) for x in row[1:1152]]
                featuresCornerQuery = [float(x) for x in queryFeature[0:1151]]
                dCorner = self.chi2_distance(
                    featuresCorner, featuresCornerQuery)
                featuresCircle = [float(x) for x in row[1153:]]
                featuresCircleQuery = [float(x) for x in queryFeature[1152:]]

                dCircle = self.chi2_distance(
                    featuresCircle, featuresCircleQuery)
                results[row[0]] = float((dCorner + dCircle*2)/3)
            f.close()
        return results

    def chi2_distance(self, histA, histB, eps=1e-10):
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                          for (a, b) in zip(histA, histB)])
        return d
