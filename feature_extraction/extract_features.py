import sys, os
from numpy.distutils.extension import fortran_pyf_ext_re
from geo_features import *
__author__ = 'mameri'

def pre_process_9geo_mean_std(feature_in_fn, feature_out_fn, feature_pre_process_txt_full_fn=''):

    feature_seq = FeatureSequence()
    if feature_seq.from_htk(feature_in_fn) != 0:
        return
    # feature_seq.to_txt(Nine_geo_out_path + '/' + feature_item+'.reg.txt')

    local_dim_features = feature_seq.num_features()
    local_num_samples = feature_seq.num_feature_vectors()

    feature_matrix = np.ndarray((local_num_samples, local_dim_features), buffer=np.array(feature_seq.sequence))
    mean = np.nanmean(feature_matrix, 0, dtype=np.float64)
    std = np.nanstd(feature_matrix, 0, dtype=np.float64)
    new_std = np.where(std == 0, 1, std)
    normalized_matrix = np.ndarray((local_num_samples, local_dim_features))

    for sample_id in range(0, local_num_samples):
        normalized_matrix[sample_id] = \
         (feature_matrix[sample_id] - mean) / new_std

    feature_seq.sequence = list(normalized_matrix)
    feature_seq.to_htk(feature_out_fn)
    if len(feature_pre_process_txt_full_fn) > 0:
        feature_seq.to_txt(feature_pre_process_txt_full_fn)



def extract_features(from_image, to_htk_fn, feature_txt_full_fn=''):
    if not os.path.exists(to_htk_fn):
        geo = GeoFeatures(from_image)
        geo.extract_features()
        geo.feature_sequence.to_htk(to_htk_fn)

        pre_process_9geo_mean_std(to_htk_fn, to_htk_fn)

        if len(feature_txt_full_fn) > 0:
            geo.feature_sequence.to_txt(feature_txt_full_fn)


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) != 2:
        print ' from.file to.file needed...'
        exit()

    from_file = argv[0]
    to_file = argv[1]
    if not os.path.exists(to_file):
        geo = GeoFeatures(from_file)
        geo.extract_features()
        geo.feature_sequence.to_htk(to_file)


    # py_txt_file = 'py.txt'
    # rb_txt_file = 'rb.txt'
    #
    # py_feature = FeatureSequence()
    # py_feature.from_htk('270-01-05.py.htk')
    # py_feature.to_txt(py_txt_file)
    #
    # rb_feature = FeatureSequence()
    # rb_feature.from_htk('270-01-05.htk')
    # rb_feature.to_txt(rb_txt_file)

