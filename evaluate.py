#!/usr/bin/env python
"""
Usage:
    evaluate.py [options]

Options:
    -h --help                        Show this screen.
    --model=NAME                     The model version
    --saved-data-dir=NAME            The path to the saved data.
    --debug                          Enable debug routines. [default: False]
    --trained-model=NAME             Path to trained model
"""
import os
import pickle

from docopt import docopt
from dpu_utils.utils import run_and_debug

from dataset import load_data_from_dir, get_minibatch_iterator
from model import SyntacticModelv2, SyntacticModelv1, SyntacticModelv3


def run(args) -> None:
    print("Loading model ...")
    if args['--model'] == 'v1':
        model = SyntacticModelv1.restore(args["--trained-model"])
    elif args['--model'] == "v2":
        model = SyntacticModelv2.restore(args["--trained-model"])
    elif args['--model'] == "v3":
        model = SyntacticModelv3.restore(args["--trained-model"])

    print(f"  Loaded trained model from {args['--trained-model']}.")

    print("Loading data ...")
    with open(os.path.join(args['--saved-data-dir'], 'seen_test_data'), 'rb') as input:
        seen_test_data = pickle.load(input)
    with open(os.path.join(args['--saved-data-dir'], 'unseen_test_data'), 'rb') as input:
        unseen_test_data = pickle.load(input)

    print(f"  Loaded {seen_test_data[0].shape[0]} seen test samples.")
    print(f"  Loaded {unseen_test_data[0].shape[0]} unseen test samples.")


    for dataset, name in zip([seen_test_data, unseen_test_data], ['seen_test_data', 'unseen_test_data']):
        test_loss, test_acc = model.run_one_epoch(
            get_minibatch_iterator(
                dataset,
                model.hyperparameters["batch_size"],
                is_training=False,
                drop_remainder=False,
            ),
            training=False,
        )
        print(f"{name}:  Loss {test_loss:.4f}, Acc {test_acc:.3f}")

if __name__ == "__main__":
    args = docopt(__doc__)
    run_and_debug(lambda: run(args), args["--debug"])
