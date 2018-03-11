
import dtw
from feature_extraction.feature_sequence import *


class DTWMatchingEngine(object):

    def __init__(self, parameter):

        self.dtw_alg = dtw.DtwDisimillarity()
        self.dtw_alg.set_beam(float(parameter))
        self.max = - 1.0
        self.feature_cache = {}

        # print 'DTW Matching created'

    def get_distance(self, source_fn, target_fn):

        if source_fn in self.feature_cache:
            feature_seq1 = self.feature_cache[source_fn]

        else:
            if not os.path.exists(source_fn):
                print 'fn not exists', source_fn

            feature_seq1 = FeatureSequence()
            if feature_seq1.from_htk(source_fn) != 0:
                print 'failed in file ', source_fn, os.path.exists(source_fn)
                return self.max
            self.feature_cache[source_fn] = feature_seq1

        self.dtw_alg.set_feature1(feature_seq1.sequence)

        if target_fn in self.feature_cache:
            feature_seq2 = self.feature_cache[target_fn]

        else:

            feature_seq2 = FeatureSequence()
            if feature_seq2.from_htk(target_fn) != 0:
                print 'failed in file', target_fn, os.path.exists(target_fn)
                return self.max
            self.feature_cache[target_fn] = feature_seq2

        self.dtw_alg.set_feature2(feature_seq2.sequence)

        # print 'calling dtw'
        [result, dtw_path, dtw_len] = self.dtw_alg.dtw_dissimilarity()

        local_num_samples1 = feature_seq1.num_feature_vectors()
        local_num_samples2 = feature_seq2.num_feature_vectors()

        if result == float('Inf'):
            distance = self.max
        else:
            distance = result / float(local_num_samples1 + local_num_samples2)

        # print distance
        # distance = 0.0
        return distance

    def __del__(self):
        pass
        # print 'DTW Matching terminated'

    @staticmethod
    def get_supported_algorithm():
        return ['dtw']


def get_matching_engine(parameter, alg_name='dtw'):
      
    if alg_name in DTWMatchingEngine.get_supported_algorithm():
        matching_engine = DTWMatchingEngine(parameter)
        return matching_engine
    else:
        raise Exception('Algorithm not supported {}'.format(alg_name))


