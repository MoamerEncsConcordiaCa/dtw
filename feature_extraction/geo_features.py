from feature_sequence import FeatureSequence
from features import *
__author__ = 'mameri'


class GeoFeatures ( Features):

    def __init__(self,image_filename):
        Features.__init__(self, image_filename)
        self.feature_sequence = FeatureSequence()

    def extract_features(self):

        self.feature_sequence = FeatureSequence()
        for x in range(0, self.width):
            # print x
            feature_vec = self.feature_vector(x)
            # print feature_vec
            self.feature_sequence.add_feature_vector(feature_vec)

    def feature_vector(self, x):
        features = []
        features.append(self.histogram(x))
        features.append(self.upper_bound(x))
        features.append(self.lower_bound(x))
        features.append(self.upper_deviation(x))
        features.append(self.lower_deviation(x))
        features.append(self.between(x))
        features.append(self.black_white_transitions(x))
        features.append(self.gravity(x))
        features.append(self.moment2(x))
        return features

    # feature 1
    def histogram(self, x):
        black_pixels = float(self.pixels_at(x, 0, self.height))
        # print x, black_pixels , self.height
        return black_pixels / self.height

    # feature 2
    def upper_bound(self, x):
        return  self.upper(x) / float(self.height)

    # feature 3
    def lower_bound(self, x):
        return self.lower(x)/ float(self.height)

    # feature 4
    def upper_deviation(self, x):
        local_value = 0.0
        if x < self.width - 1:
            local_value = float(self.upper(x) - self.upper(x + 1))
        return  local_value

    # feature 5
    def lower_deviation(self, x):
        local_value = 0.0
        if x < self.width - 1:
            local_value = float(self.lower(x) - self.lower(x + 1))
        return local_value

    # feature 6
    def between(self,x):
        u = self.upper(x)
        l = self.lower(x)
        local_value = 0.0
        if u + 1 < l:
            local_value = self.pixels_at(x, u, l) / float(l - u)

        return local_value

    # feature 7
    def black_white_transitions(self, x):
        local_flag = False
        local_transition = 0
        for y in range (0, self.height):
            if not local_flag and self.is_black(self.grayscale_value_at(x, y )):
                local_transition += 1
                local_flag = True
            elif local_flag and self.is_white(self.grayscale_value_at(x,y)):
                local_flag = False

        return local_transition

    # feature 8
    def gravity(self, x):
        local_grav = 0.0
        for y in range(0, self.height):
            local_d = self.height / 2.0 - y
            local_grav += local_d * (1.0 - self.grayscale_value_at(x, y)/ float(self.WHITE))

        return local_grav / float(self.height)

    # feature 9
    def moment2(self,x):
        local_mom2 = 0.0
        for y in range(0, self.height):
            local_mom2 += (y*y) * (1.0 - self.grayscale_value_at(x, y)/float(self.WHITE))

        return local_mom2 / (self.height * self.height)

    # feature helpers
    def pixels_at(self, x, upper_bound, lower_bound):
        pixels = 0.0
        for y in range(upper_bound, lower_bound):
            if self.is_black(self.grayscale_value_at(x, y)):
                pixels += 1
        return pixels

    def upper(self, x):
        y = 0
        while y < self.height and self.is_white(self.grayscale_value_at(x, y)):
            y += 1
        return y

    def lower(self, x):#
        y = self.height - 1
        while y > 0 and self.is_white(self.grayscale_value_at(x,y)):
            y -= 1
        return y
