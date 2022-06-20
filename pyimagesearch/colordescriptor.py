import numpy as np
import cv2
import imutils


class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins

    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w*0.5), int(h*0.5))  # tâm
        segments = [(0, cX, 0, cY), (cX, w, 0, cY),
                    (cX, w, cY, h), (0, cX, cY, h)]
        """ (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2) """
        radiusCircleMask = 380  # ban kinh
        circleMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.circle(circleMask, (cX, cY), radiusCircleMask, 255, -1)
        """ cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1) """
        # tính hist ở các bên rìa
        for(startX, endX, startY, endY) in segments:
            cornerMask = np.zeros(image.shape[:2], dtype='uint8')
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, circleMask)
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        # tính hist trong vòng tròn
        for(startX, endX, startY, endY) in segments:
            rectangleMask = np.zeros(image.shape[:2], dtype='uint8')
            cv2.rectangle(rectangleMask, (startX, startY),
                          (endX, endY), 255, -1)
            cornerMask = cv2.subtract(rectangleMask, circleMask)
            quarterCircleMask = cv2.subtract(rectangleMask, cornerMask)
            hist = self.histogram(image, quarterCircleMask)
            features.extend(hist)
        """ hist = self.histogram(image, circleMask)
        features.extend(hist) """
        return features

    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 360, 0, 256, 0, 256])
        if(imutils.is_cv2()):
            hist = cv2.normalize(hist).flatten()
        else:
            hist = cv2.normalize(hist, hist).flatten()
        return hist
