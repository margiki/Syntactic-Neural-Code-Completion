#!/usr/bin/env python
"""
Usage:
    test_tensorise_sequence.py [options] DATA_DIR

Options:
    -h --help                        Show this screen.
    --max-num-files INT              Number of files to load.
    --debug                          Enable debug routines. [default: False]
"""
from docopt import docopt
from dpu_utils.utils import run_and_debug

import os, sys
# Add parent directory dynamically
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from dataset import build_vocab_from_data_dir, load_data_from_dir


def find_first(item, vector):
    """return the index of the first occurence of item in vector"""
    for i in range(len(vector)):
        if item == vector[i]:
            return i
    return len(vector)


def run(arguments) -> None:
    vocab_nodes, vocab_actions = build_vocab_from_data_dir(
        [arguments["DATA_DIR"]],
        vocab_size=500,
        max_num_files=arguments.get("--max-num-files"),
    )
    tensorised_nodes, tensorised_actions, _ = load_data_from_dir(
        vocab_nodes,
        vocab_actions,
        length=50,
        data_dirs=[arguments["DATA_DIR"]],
        max_num_files=arguments.get("--max-num-files"),
    )

    for idx in range(min(5, len(tensorised_actions))):
        token_ids = tensorised_actions[idx]
        length = find_first(
            vocab_actions.get_id_or_unk(vocab_actions.get_pad()), token_ids
        )
        tokens = [vocab_actions.get_name_for_id(tok_id) for tok_id in token_ids]
        print("Sample %i:" % (idx))
        print(" Real length: %i" % (length))
        print(" Tensor length: %i" % (len(token_ids)))
        print(" Raw tensor: %s (truncated)" % (str(token_ids[: length + 2])))
        print(" Interpreted tensor: %s (truncated)" % (str(tokens[: length + 2])))


if __name__ == "__main__":
    args = docopt(__doc__)
    run_and_debug(lambda: run(args), args["--debug"])
