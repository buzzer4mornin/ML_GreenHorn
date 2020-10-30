#!/usr/bin/env python3
import argparse
import lzma
import pickle
import os
import urllib.request
import sys
import argparse
import lzma
import os
import pickle
import urllib.request
import numpy as np
import pandas as pd
from sklearn import svm, metrics
import time
import matplotlib.pyplot as plt
import seaborn as sn
import sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
from sklearn.utils import check_random_state

class Dataset:
    """MNIST Dataset.
    The train set contains 60000 images of handwritten digits. The data
    contain 28*28=784 values in range 0-255, the targets are numbers 0-9.
    """
    def __init__(self,
                 name="mnist.train.npz",
                 url="https://ufal.mff.cuni.cz/~straka/courses/npfl129/2021/datasets/"):
        if not os.path.exists(name):
            print("Downloading dataset {}...".format(name), file=sys.stderr)
            urllib.request.urlretrieve(url + name, filename=name)

        # Load the dataset, i.e., `data` and optionally `target`.
        dataset = np.load(name)
        for key, value in dataset.items():
            setattr(self, key, value)
        self.data = self.data.reshape([-1, 28*28]).astype(np.float)


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--predict", default=None, type=str, help="Run prediction on given data")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--model_path", default="mnist_competition.model", type=str, help="Model path")

""" LOGISTIC REGRESSION: https://scikit-learn.org/stable/auto_examples/linear_model/plot_sparse_logistic_regression_mnist.html"""
"""SVM https://www.kaggle.com/nishan192/mnist-digit-recognition-using-svm"""

def main(args):
    if args.predict is None:
        # We are training a model.
        np.random.seed(args.seed)
        train = Dataset()

        train_samples = 5000
        X = pd.DataFrame(train.data)
        y = pd.DataFrame(train.target)
        #print(y.value_counts())
        print(X.shape)


        #TODO: split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                            random_state=args.seed, shuffle=True)
        y_train = np.asarray(y_train).ravel()
        y_test = np.asarray(y_test).ravel()

        #TODO: normalize data
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        #help(LogisticRegression)



        #TODO: Logistic Regression setup
        '''clf = LogisticRegression(
            C=50. / train_samples, penalty='l2', solver='saga', tol=0.01, class_weight='balanced'
        )
        clf.fit(X_train, y_train)
        sparsity = np.mean(clf.coef_ == 0) * 100
        score = clf.score(X_test, y_test)
        # print('Best C % .4f' % clf.C_)
        print("Sparsity with L1 penalty: %.2f%%" % sparsity)
        print("Test score with L1 penalty: %.4f" % score)'''

        #TODO: SVM setup
        #classifier = svm.SVC(
        #    C=1, kernel='rbf', degree=3, tol=0.1, class_weight='balanced', gamma=0.001
        #)
        classifier = svm.SVC(kernel='linear', C=10, gamma=0.001)

        classifier.fit(X_train, y_train)
        # Now predict the value of the digit on the second half:
        predicted = classifier.predict(X_test)
        score = classifier.score(X_test, y_test)
        print("Test score with L1 penalty: %.4f" % score)



        # TODO: Train a model on the given dataset and store it in `model`.
        model = None

        # If you trained one or more MLPs, you can use the following code
        # to compress it significantly (approximately 12 times). The snippet
        # assumes the trained MLPClassifier is in `mlp` variable.
        # mlp._optimizer = None
        # for i in range(len(mlp.coefs_)): mlp.coefs_[i] = mlp.coefs_[i].astype(np.float16)
        # for i in range(len(mlp.intercepts_)): mlp.intercepts_[i] = mlp.intercepts_[i].astype(np.float16)

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