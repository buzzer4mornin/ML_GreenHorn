#!/usr/bin/env python3

# Team:
# 2f67b427-a885-11e7-a937-00505601122b
# b030d249-e9cb-11e9-9ce9-00505601122b
# 3351ff04-3f62-11e9-b0fd-00505601122b


import argparse
import lzma
import os
import pickle
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import sklearn
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


class Dataset:
    """Thyroid Dataset.
    The dataset contains real medical data related to thyroid gland function,
    classified either as normal or irregular (i.e., some thyroid disease).
    The data consists of the following features in this order:
    - 15 binary features
    - 6 real-valued features
    The target variable is binary, with 1 denoting a thyroid disease and
    0 normal function.
    """

    def __init__(self,
                 name="thyroid_competition.train.npz",
                 url="https://ufal.mff.cuni.cz/~straka/courses/npfl129/2021/datasets/"):
        if not os.path.exists(name):
            print("Downloading dataset {}...".format(name))
            urllib.request.urlretrieve(url + name, filename=name)

        # Load the dataset and return the data and targets.
        dataset = np.load(name)
        for key, value in dataset.items():
            setattr(self, key, value)


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--predict", default=None, type=str, help="Run prediction on given data")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--model_path", default="thyroid_competition.model", type=str, help="Model path")


def main(args):
    if args.predict is None:
        # We are training a model.
        np.random.seed(args.seed)
        train = Dataset()
        X = train.data
        y = train.target

        # convert to DataFrame
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)

        # ==================================================================================================
        'Explanatory Data Analysis'

        # first 15 features are Binary, remaining 6 features are Real-valued
        # for line in range(min(X.shape[0], 5)):
        #    print(" ".join("{:.4g}".format(X.loc[line, column]) for column in range(min(X.shape[1], 60))))

        # print(X.info()) # No NULL values.

        # X = X.iloc[:, 15:21]
        # print(X.describe()) # all real-valued features are in [0,1] interval. So, no need for normalization

        # print(y.iloc[:, 0].value_counts()) # dataset is extremely imbalanced {0:3488, 1:284}

        # X = train.data
        # y = train.target
        # df = pd.DataFrame(np.c_[X, y])
        # corrMatrix = df.corr()
        # sn.heatmap(corrMatrix, annot=True)
        # plt.show()      # 18/20 columns have 0.77 correlation, delete one of them

        # ==================================================================================================
        #X = X.iloc[:, :-1]

        '''X_bool = X.loc[:, 0:14]
        X_real = X.loc[:, 15:21]

        poly = PolynomialFeatures(2, include_bias=False)
        start_col = X_real.shape[1]
        X_real = pd.DataFrame(poly.fit_transform(X))
        X_real = X_real.iloc[:, start_col:]

        X = np.c_[X_real, X_bool]'''

        #poly = PolynomialFeatures(2, include_bias=False)
        #start_col = X.shape[1]
        #X = pd.DataFrame(poly.fit_transform(X))
        #X = X.iloc[:, start_col:]


        normalizer = StandardScaler()
        X.iloc[:, 15:21] = normalizer.fit_transform(X.iloc[:, 15:21])
        X = normalizer.fit_transform(X)


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                            random_state=args.seed, shuffle=True)

        y_train = np.asarray(y_train).ravel()
        y_test = np.asarray(y_test).ravel()
        clf = LogisticRegression(random_state=args.seed, solver="liblinear",
                                 class_weight="balanced", tol=1e-2, penalty='l1').fit(X_train, y_train)

        predicted_Y = clf.predict(X_test)
        count = 0
        for i, j in zip(predicted_Y, y_test):
            if i == j: count += 1

        print(count / y_test.shape[0])
        # ==================================================================================================
        '''# Prepare K-fold cross validation and find average RMSE
        X = np.asarray(X)
        y = np.asarray(y)
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        all_pairs = kf.split(X)

        explicit_rmse = 0
        for train_indices, test_indices in all_pairs:
            train_data = X[train_indices]
            test_data = X[test_indices]
            train_target = y[train_indices]
            test_target = y[test_indices]

            train_target = np.asarray(train_target).ravel()
            test_target = np.asarray(test_target).ravel()
            clf = LogisticRegression(random_state=args.seed, solver="liblinear", penalty='l1',
                                     class_weight="balanced", tol=1e-2).fit(train_data, train_target)
            predicted_Y = clf.predict(test_data)
            count = 0
            for i, j in zip(predicted_Y, test_target):
                if i == j: count += 1

            explicit_rmse += count / test_target.shape[0]

        avg_rmse = explicit_rmse / kf.n_splits
        print(avg_rmse)'''

        # ==================================================================================================


        # TODO: Train a model on the given dataset and store it in `model`.
        model = None

        # Serialize the model.
        with lzma.open(args.model_path, "wb") as model_file:
            pickle.dump(model, model_file)

    else:
        # Use the model and return test set predictions, as either a Python list or a NumPy array.
        test = Dataset(args.predict)

        with lzma.open(args.model_path, "rb") as model_file:
            model = pickle.load(model_file)

        # TODO: Generate `predictions` with the test set predictions.
        predictions = None

        return predictions


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)
