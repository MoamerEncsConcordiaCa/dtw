import os
from matching_engine import get_matching_engine
from feature_extraction.extract_features import *

if __name__ == '__main__':

    # set the band parameter of dtw
    dtw_engine = get_matching_engine(0.05, 'dtw')

    img_dir = 'data/img'
    feature_dir = 'data/features'

    # feature extraction
    for img in os.listdir(img_dir):
        img_fn = os.path.join(img_dir, img)
        feature_fn = os.path.join(feature_dir, img.replace('.png', '.htk'))
        extract_features(img_fn,feature_fn)

    # dtw matching
    for feature_fn_1 in os.listdir(feature_dir):
        for feature_fn_2 in os.listdir(feature_dir):
            f1full = os.path.join(feature_dir, feature_fn_1)
            f2full = os.path.join(feature_dir, feature_fn_2)
            print feature_fn_1, feature_fn_2, 'dtw=', dtw_engine.get_distance(f1full, f2full)

