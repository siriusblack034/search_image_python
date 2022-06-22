import numpy as np
import csv
from scipy.spatial import distance


class Distance:
    def __init__(self, indexPath):
        self.indexPath = indexPath

    def distance(self, queryFeature):
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
