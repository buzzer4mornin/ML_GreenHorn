#!/usr/bin/env python3

# Team:
# 2f67b427-a885-11e7-a937-00505601122b
# b030d249-e9cb-11e9-9ce9-00505601122b
# 3351ff04-3f62-11e9-b0fd-00505601122b

import argparse
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--data_size", default=10, type=int, help="Data size")
parser.add_argument("--range", default=3, type=int, help="Feature order range")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
parser.add_argument("--test_size", default=0.5, type=lambda x:int(x) if x.isdigit() else float(x), help="Test set size")
# If you add more arguments, ReCodEx will keep them with your default values.

def main(args):
    # Create the data
    xs = np.linspace(0, 7, num=args.data_size)
    ys = np.sin(xs) + np.random.RandomState(args.seed).normal(0, 0.2, size=args.data_size)
    xs = xs.reshape(-1, 1)
    xs_copy = xs

    rmses = []
    for order in range(1, args.range + 1):
        # TODO: Create features of x^1, ..., x^order.
        if order != 1:
            add = xs_copy**order
            xs = np.c_[xs, add]

        # TODO: Split the data into a train set and a test set.
        # Use `sklearn.model_selection.train_test_split` method call, passing
        # arguments `test_size=args.test_size, random_state=args.seed`.
        X_train, X_test, Y_train, Y_test = train_test_split(xs, ys, test_size=args.test_size,
                                                            random_state=args.seed)

        # TODO: Fit a linear regression model using `sklearn.linear_model.LinearRegression`.
        reg = LinearRegression()
        reg.fit(X_train, Y_train)

        # TODO: Predict targets on the test set using the trained model.
        predicted_Y = reg.predict(X_test)

        # TODO: Compute root mean square error on the test set predictions
        rmse = np.sqrt(sklearn.metrics.mean_squared_error(predicted_Y, Y_test))

        rmses.append(rmse)

    return rmses

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    rmses = main(args)
    for order, rmse in enumerate(rmses):
        print("Maximum feature order {}: {:.2f} RMSE".format(order + 1, rmse))