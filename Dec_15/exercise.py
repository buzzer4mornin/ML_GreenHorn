import argparse
import numpy as np
import sklearn.datasets
import sklearn.metrics
import sklearn.model_selection

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--criterion", default="gini", type=str, help="Criterion to use; either `gini` or `entropy`")
parser.add_argument("--max_depth", default=None, type=int, help="Maximum decision tree depth")
parser.add_argument("--max_leaves", default=None, type=int, help="Maximum number of leaf nodes")
parser.add_argument("--min_to_split", default=2, type=int, help="Minimum examples required to split")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=42, type=int, help="Random seed")
parser.add_argument("--test_size", default=42, type=lambda x:int(x) if x.isdigit() else float(x), help="Test set size")
# If you add more arguments, ReCodEx will keep them with your default values.


def main(args):

    X = np.array([1, 7, 3, 3, 3, 5, 6, 7]).reshape(-1, 1)
    y = np.array([0, 1, 2, 2, 2, 2, 3, 1])

    def best_split(args, X, y):

        # Need at least two elements to split a node.
        if len(y) < args.min_to_split:
            return None, None

        # Count of each class in the current node.
        num_parent = [np.sum(y == c) for c in range(4)]
        print(num_parent)


        # Gini/Entropy of current node.
        if args.criterion == "gini":
            best_gini = sum((n / len(y)) * (1 - (n / len(y))) for n in num_parent)
        else:
            best_gini = -1 * sum((n / len(y)) * np.log(n / len(y)) for n in num_parent if (n / len(y)) != 0)

        print("initial {}:".format(args.criterion), best_gini, "\n=====================")
        best_idx, best_thr = None, None

        # Loop through all features.
        for idx in range(1):
            # Sort data along selected feature.
            thresholds, classes = zip(*sorted(zip(X[:, idx], y)))
            print(thresholds, classes)

            num_left = [0] * 4
            num_right = num_parent.copy()

            # Possible split positions
            for i in range(1, len(y)):
                c = classes[i - 1]
                num_left[c] += 1
                num_right[c] -= 1
                if args.criterion == "gini":
                    gini_left = sum((num_left[x] / i) * (1 - (num_left[x] / i)) for x in range(4))
                    gini_right = sum((num_right[x] / (len(y) - i)) * (1 - (num_right[x] / (len(y) - i))) for x in range(4))
                else:
                    gini_left = -1 * sum((num_left[x] / i) * np.log(num_left[x] / i) for x in range(4) if (num_left[x] / i) != 0)
                    gini_right = -1 * sum((num_right[x] / (len(y) - i)) * np.log((num_right[x] / (len(y) - i))) for x in range(4) if (num_right[x] / (len(y) - i)) != 0)

                # The Gini/Entropy of a split is the weighted average of children
                gini = (i * gini_left + (len(y) - i) * gini_right) / len(y)

                # The following condition is to make sure we don't try to split two
                # points with identical values for that feature, as it is impossible
                # (both have to end up on the same side of a split).
                if thresholds[i] == thresholds[i - 1]:
                    continue

                if gini < best_gini:
                    best_gini = gini
                    best_idx = idx
                    best_thr = (thresholds[i] + thresholds[i - 1]) / 2  # midpoint

        return best_idx, best_thr

    a, b = best_split(args,X, y)

    return a,b



if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    a, b = main(args)
    print("=====================\n", "split index vs point", a, b)