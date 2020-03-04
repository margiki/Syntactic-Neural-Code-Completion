"""
Usage:
    hyper_parameter_search.py [options]

*_DATA_DIR are directories filled with files that we use as data.

Options:
    -h
    --model=NAME
    --save-dir=NAME                 Save the models path
    --saved-data-dir=NAME           Location of already computed data directory.
    --log-file=NAME
    --log-file-hyperparams=NAME
    --tensorboard-logs-path=NAME    Path to tensorboard logs
    --compute-data
"""

import json
import os
from datetime import datetime

import git
from docopt import docopt

import train as train
from evaluate import evaluate

if __name__ == "__main__":
    print("Started")

    args = docopt(__doc__)
    args['--max-num-epochs'] = 300
    args['--patience'] = 5

    with open(os.path.join(args['--log-file-hyperparams'], 'hyper_params.log'), 'a') as log_file_hyper_params:

        log_file_hyper_params.write(str(datetime.now()))
        log_file_hyper_params.write(f"  {args['--model']}  ")
        log_file_hyper_params.write(git.Repo(search_parent_directories=True).head.object.hexsha)
        log_file_hyper_params.write("\n")
        log_file_hyper_params.write("%15s  |  %15s  |  %15s  |  %15s  |  %15s  |  %15s  | %15s\n" %
                                    ("node_embedding", "action_embedding", "rnn_hidden_dim_1",
                                     "rnn_hidden_dim_2", "learning_rate", "validation_accuracy", "run_name"))

        # Model v1
        action_embeddings = [64, 96, 128]
        node_embedding = [16, 32, 64]
        rnn_hidden_dim_1s = [64, 96, 128]
        rnn_hidden_dim_2s = [64, 96, 128]
        learning_rates = [0.005, 0.01]

        if args['--model'] == 'v1':
            for action_embedding in action_embeddings:
                for rnn_hidden_dim_1 in rnn_hidden_dim_1s:
                    for learning_rate in learning_rates:
                        hyper_param_override = {
                            'action_embedding': action_embedding,
                            'rnn_hidden_dim_1': rnn_hidden_dim_1,
                            'learning_rate': learning_rates,
                            '--run-name': f'rnn_best_model__ae{action_embedding}__rnn1{rnn_hidden_dim_1}__lr{learning_rate}'
                        }

                        args_copy = args.copy()
                        args_copy.update(hyper_param_override)
                        print(args_copy)

                        train.run(args_copy)

                        run_name = f"{hyper_param_override['--run-name']}_best_model.bin"
                        accs = evaluate({
                            '--model': args['--model'],
                            '--saved-data-dir': args['--saved-data-dir'],
                            '--trained-model': os.path.join(args['--save-dir'], run_name)
                        })

                        log_file_hyper_params.write("%15s  |  %15s  |  %15s  |  %15s  |  %15s  |  %15s  | %15s\n" %
                                                    ("-", action_embedding, rnn_hidden_dim_1,
                                                     "-", learning_rate, accs[1].numpy(),
                                                     run_name))

        # Model v2
        if args['--model'] == 'v2':
            exit(0)

        # Model v3

        if args['--model'] == 'v3':
            exit(0)
