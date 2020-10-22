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
        #for line in range(min(X.shape[0], 5)):
        #    print(" ".join("{:.4g}".format(X.loc[line, column]) for column in range(min(X.shape[1], 60))))

        #print(X.info()) # No NULL values.


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