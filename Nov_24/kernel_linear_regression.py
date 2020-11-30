#!/usr/bin/env python3
import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np
import sklearn.metrics


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--batch_size", default=1, type=int, help="Batch size")
parser.add_argument("--data_size", default=50, type=int, help="Data size")
parser.add_argument("--kernel", default="rbf", type=str, help="Kernel type [poly|rbf]")
parser.add_argument("--kernel_degree", default=3, type=int, help="Degree for poly kernel")
parser.add_argument("--kernel_gamma", default=1.0, type=float, help="Gamma for poly and rbf kernel")
parser.add_argument("--iterations", default=200, type=int, help="Number of training iterations")
parser.add_argument("--l2", default=0.0, type=float, help="L2 regularization weight")
parser.add_argument("--learning_rate", default=0.01, type=float, help="Learning rate")
parser.add_argument("--plot", default=False, const=True, nargs="?", type=str, help="Plot the predictions")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
# If you add more arguments, ReCodEx will keep them with your default values.

def main(args):
    # Create a random generator with a given seed
    generator = np.random.RandomState(args.seed)

    # Generate an artifical regression dataset
    train_data = np.linspace(-1, 1, args.data_size)
    train_targets = np.sin(5 * train_data) + generator.normal(scale=0.25, size=args.data_size) + 1


    test_data = np.linspace(-1.2, 1.2, 2 * args.data_size)
    test_targets = np.sin(5 * test_data) + 1



    betas = np.zeros(args.data_size)


    # TODO: Perform `args.iterations` of SGD-like updates, but in dual formulation
    # using `betas` as weights of individual training examples.

    # We assume the primary formulation of our model is
    #   y = phi(x)^T w + bias
    # and the loss in the primary problem is batched MSE with L2 regularization:
    #   L = sum_{i \in B} 1/|B| * [1/2 * (phi(x_i)^T w + bias - target_i)^2] + 1/2 * args.l2 * w^2

    # For `bias`, use explicitly the average of the training targets, and do
    # not update it futher during training.

    # Instead of using feature map `phi` directly, we use a given kernel computing
    #   K(x, y) = phi(x)^T phi(y)
    # We consider the following `args.kernel`s:
    # - "poly": K(x, y; degree, gamma) = (gamma * x^T y + 1) ^ degree
    # - "rbf": K(x, y; gamma) = exp^{- gamma * ||x - y||^2}

    def kernel (x1, x2):
        return [(args.kernel_gamma * np.dot(x1, x2) + 1) ** args.kernel_degree if args.kernel == "poly"
                else np.exp(-1 * args.kernel_gamma * np.abs(x1 - x2) ** 2)]

    # After each iteration, compute RMSE both on training and testing data.
    train_rmses, test_rmses = [], []

    bias = np.mean(train_targets)

    for iteration in range(args.iterations):
        permutation = generator.permutation(train_data.shape[0])

        # TODO: Process the data in the order of `permutation`, performing
        # batched updates to the `betas`. You can assume that `args.batch_size`
        # exactly divides `train_data.shape[0]`.

        gradient_components = 0
        bi_arr = []
        for i in permutation:
            sums = 0
            for j in permutation:
                sums += betas[j]*kernel(train_data[i], train_data[j])[0]
            bi = betas[i] + args.learning_rate * (train_targets[i] - sums - bias) / args.batch_size - args.l2 * args.learning_rate * betas[i]
            bi_arr.append(bi)
            gradient_components += 1
            if gradient_components == args.batch_size:
                arr = []
                for k in range(len(bi_arr) - args.batch_size, len(bi_arr)):
                    betas[permutation[k]] = bi_arr[k]
                    arr.append(permutation[k])
                for z in permutation:
                    if z not in arr:
                        betas[z] = betas[z] - args.l2 * args.learning_rate * betas[z]
                gradient_components = 0
        assert gradient_components == 0


        # TODO: Append RMSE on training and testing data to `train_rmses` and
        # `test_rmses` after the iteration.

        #print(len(train_data), len(test_data))

        my_test = []
        for i in range(len(test_data)):
            sums = 0
            for j in range(len(betas)):
                sums += betas[j] * kernel(test_data[i], train_data[j])[0]
            my_test.append(sums + bias)

        my_train = []
        for i in range(len(train_data)):
            sums = 0
            for j in range(len(betas)):
                sums += betas[j] * kernel(train_data[i], train_data[j])[0]
            my_train.append(sums + bias)

        test_rmses.append(np.sqrt(sklearn.metrics.mean_squared_error(np.array(test_targets), np.array(my_test))))
        train_rmses.append(np.sqrt(sklearn.metrics.mean_squared_error(np.array(train_targets), np.array(my_train))))

        if (iteration + 1) % 10 == 0:
            print("Iteration {}, train RMSE {:.2f}, test RMSE {:.2f}".format(
                iteration + 1, train_rmses[-1], test_rmses[-1]))

    return train_rmses, test_rmses

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)