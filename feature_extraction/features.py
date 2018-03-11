from abc import ABCMeta, abstractmethod

# from pylab import *
from matplotlib.image import *
import numpy as np

from feature_sequence import *

__author__ = 'mameri'


class Features:
    __metaclass__ = ABCMeta
    WHITE = 255.0
    ALMOST_WHITE = 200.0

    def __init__(self, image_filename):

        # self.image = Image.open(image_filename).convert('L')
        # [self.width, self.height] = self.image.size
        # # array(self.image.getdata()).reshape(self.image.size)

        self.feature_sequence = FeatureSequence()
        self.image_matrix = imread(image_filename)
        # print self.image_matrix.shape
        self.image_matrix = self.image_matrix.transpose()
        # print max(self.image_matrix[:][0])
        # print self.image_matrix.shape
        self.image_matrix = np.uint8(self.image_matrix * 255)
        # import matplotlib.pyplot as plt
        # plt.imshow(self.image_matrix)
        # plt.show()

        [self.width, self.height] = self.image_matrix.shape
        # print self.image_matrix.dtype
        # print 'image height', len(self.image_matrix[self.width - 1])
        # print 'xrange width :', self.width

    @abstractmethod
    def extract_features(self):
        pass

    def grayscale_value_at(self, x, y):
        return self.image_matrix[x][y]

    def grayscale_white_border(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return 255
        return self.image_matrix[x][y]

    def is_black(self, grayscale_value):
        # print grayscale_value
        return grayscale_value < Features.ALMOST_WHITE

    def is_white(self, grayscale_value):
        return grayscale_value > Features.ALMOST_WHITE




