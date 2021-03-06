import glob
import logging
import os

import numpy
import pandas
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV


def pretty_print_dict(dictionary):
    return '\n'.join(['%s:: %s' % (key, value) for (key, value) in dictionary.items()])


def ensure_dir(dir_name):
    """
    Function checks if there is a directory with specified dir_name
    if not, it is not existing, dir structure is created

    :param dir_name:
    """
    directory = os.path.dirname(dir_name)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_names_by_ext(path, extension='pkl'):
    """
    Method returns list of files with specified extension
    in directory

    :param path: directory
    :param extension: file_extension
    """
    files_grabbed = []
    files_grabbed.extend(glob.glob(path + os.sep + "*." + extension))
    return files_grabbed


def log_train_results_CV(rs, X_validation, Y_validation):
    logging.info("CV results:")
    logging.info(rs.cv_results_)
    logging.info("Best estimator:")
    logging.info(rs.best_estimator_)
    logging.info("Best params:")
    logging.info(rs.best_params_)
    logging.info("Real / Predicted values:")
    mlp_output_values_scaled = rs.predict(X_validation)
    logging.info(pandas.DataFrame({'predicted': mlp_output_values_scaled, 'real': Y_validation}))


def get_redundant_pairs(data_frame):
    pairs_to_drop = set()
    cols = data_frame.columns
    for i in range(0, data_frame.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop


def get_top_abs_correlations(data_frame, n=5):
    au_corr = data_frame.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(data_frame)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]


def get_correlations_by_feature(data_frame, feature_name):
    feature_corr = data_frame.corr()[feature_name]
    feature_corr = feature_corr.drop(labels=feature_name)
    feature_corr = feature_corr.reindex(feature_corr.abs().sort_values(ascending=False).index)
    return feature_corr


def exclude_boundary_values(data_set, feature_name, scale):
    return data_set[
        numpy.abs(data_set[feature_name] - data_set[feature_name].mean()) <= (scale * data_set[feature_name].std())]


def refactor_data_set_to_numeric(data_set):
    data_set = data_set.apply(pandas.to_numeric, errors="coerce")
    data_set.dropna(axis=1, how="all", inplace=True)
    return data_set


def transform_data_frame(scaler, data_frame):
    return pandas.DataFrame(scaler.transform(data_frame), columns=data_frame.columns)


def inverse_transform_data_frame(scaler, data_frame):
    return pandas.DataFrame(scaler.inverse_transform(data_frame), columns=data_frame.columns)


def fit_transform_data_frame(scaler, data_frame):
    return pandas.DataFrame(scaler.fit_transform(data_frame), columns=data_frame.columns)


def exclude_data_frame_columns(data_frame, columns_to_drop):
    out_put_data_frame = data_frame.copy()
    out_put_data_frame.drop(columns_to_drop, axis="columns", inplace=True)
    return out_put_data_frame
