import struct
import os

__author__ = 'mameri'

class FeatureSequence:
    def __init__(self):
        self.sequence = []

    def feature_vector_sequence(self):
        return self.sequence

    def add_feature_vector(self, feature_vector):
        self.sequence.append(feature_vector)

    def num_feature_vectors(self):
        return len(self.sequence)

    def num_features(self):
        return len(self.sequence[0])

    def from_htk(self, htk_filename):
        if not os.path.exists(htk_filename):
            return 1

        with open(htk_filename, 'rb') as f_h:
            header_bytes = f_h.read(12)
            header_values = struct.unpack('<iihh', header_bytes)
            [num_samples, dummy_rate, n_features, sample_kind] = header_values
            # print header_values
            n_features /= 4

            for idx_sample in range(0, num_samples):
                feature_vector = []
                feature_vector.extend(struct.unpack('<'+'f' * n_features, f_h.read(n_features * 4)))
                self.add_feature_vector(feature_vector)

            # print self.sequence
        return 0

    def to_htk(self, htk_filename):

        num_samples = self.num_feature_vectors()
        sample_size_bytes = self.num_features() * 4
        sample_size_num = self.num_features()
        header_bytes = struct.pack('<iihh', num_samples, 1, sample_size_bytes, 9)

        with open(htk_filename, 'wb') as f_h:
            f_h.write(header_bytes)
            for feature_vector in self.sequence:
                f_h.write(struct.pack('<' + 'f' * sample_size_num,  *feature_vector))
                # for feature_item in feature_vector:

        return 0

    def to_txt(self, txt_filename):
        num_samples = self.num_feature_vectors()
        sample_size_bytes = self.num_features() * 4
        sample_size_num = self.num_features()
        header_bytes = (num_samples, 1, sample_size_bytes, 9)
        with open(txt_filename, 'w') as f_h:
            f_h.write(str(header_bytes) + '\n')
            for feature_vector in self.sequence:
                f_h.write(str(feature_vector[:]) +'\n')

        return 0



if __name__ == "__main__":

    a = FeatureSequence()
    a.from_htk('sample.htk')
    a.to_htk('to.htk')


