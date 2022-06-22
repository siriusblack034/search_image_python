
import os
import cv2
import numpy as np
from numpy import linalg as LA


class ShapeDescriptor:
    def __init__(self, bins):
        self.bins = bins

    def describe(self, imagePath, cell_size=10, block_size=2):
        image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(src=image, dsize=(150, 150))
        h, w = image.shape
        # gradient
        xkernel = np.array([[-1, 0, 1]])  # filter 1 chiều
        ykernel = np.array([[-1], [0], [1]])  # chuyển vị của y
        dx = cv2.filter2D(image, cv2.CV_32F, xkernel)  # đạo hàm theo x
        dy = cv2.filter2D(image, cv2.CV_32F, ykernel)  # đạo hàm theo y
        # histogram
        magnitude = np.sqrt(np.square(dx) + np.square(dy))  # tính biên độ
        # tính góc theo radian
        orientation = np.arctan(np.divide(dy, dx+0.00001))
        orientation = np.degrees(orientation)  # đổi ra góc -90 -> 90
        orientation += 90  # 0->180

        num_cell_x = w // cell_size  # 15 cell
        num_cell_y = h // cell_size  # 15 cell
        hist_tensor = np.zeros([num_cell_y, num_cell_x, self.bins])
        for cx in range(num_cell_x):
            for cy in range(num_cell_y):
                ori = orientation[cy*cell_size:cy*cell_size +
                                  cell_size, cx*cell_size:cx*cell_size+cell_size]
                mag = magnitude[cy*cell_size:cy*cell_size +
                                cell_size, cx*cell_size:cx*cell_size+cell_size]
                hist, bin_edges = np.histogram(ori, bins=self.bins, range=(
                    0, 180), weights=mag)  # 1-D vector, 9 bins
                hist_tensor[cy, cx, :] = hist
            pass
        pass
        # normalization l2-norm
        redundant_cell = block_size-1
        # mask 2x2 for overlap
        feature_tensor = np.zeros(
            [num_cell_y-redundant_cell, num_cell_x-redundant_cell, block_size*block_size*self.bins])
        for bx in range(num_cell_x-redundant_cell):  # 14
            for by in range(num_cell_y-redundant_cell):  # 14
                by_from = by
                by_to = by+block_size
                bx_from = bx
                bx_to = bx+block_size
                v = hist_tensor[by_from:by_to, bx_from:bx_to,
                                :].flatten()  # to 1-D array (vector)
                feature_tensor[by, bx, :] = v / LA.norm(v, 2)
                # avoid NaN:
                # avoid NaN (zero division)
                if np.isnan(feature_tensor[by, bx, :]).any():
                    feature_tensor[by, bx, :] = v
        return feature_tensor.flatten()  # 14x14x36 = 7056 pt
