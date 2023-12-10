import argparse
import tempfile
from pathlib import Path
from pprint import pprint

from Tweezer.GhidraBridge.ghidra_bridge import GhidraBridge
from Tweezer.Model.model import Model
from Tweezer.Training.trainer import Trainer


class Tweezer():
    def __init__(self, model_path="TweezerMDL"):
        self.model = None
        self.model_path = model_path

    def setup_model(self, list_of_binary_folders):
        self.extend_model_training(list_of_binary_folders)

    def extend_model_training(self, list_of_binary_folders):
        trainer = Trainer()
        self.model = Model(self.model_path)
        with tempfile.TemporaryDirectory() as decom_output:
            trainer._generate_decompiled_functions_from_binaries(list_of_binary_folders, decom_output)
            self.model.get_vectors_from_files(decom_output)

    def find_closest_functions(self, function_file, number_of_closest =10):
        self.model = Model(self.model_path)
        self.model.find_similar_vectors(
            self.model._function_file_to_vec(function_file),number_of_closest)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command-line interface Tweezer, binary analysis unknown function name finder.')

    # Model path argument (always required)
    parser.add_argument('--model-path', required=True, help='Path to the Tweezer model file')
    # Binary locations argument (accepts multiple values)
    parser.add_argument('--binary-locations', nargs='+', help='List of binary locations to train/extend training off')

    # Create a mutually exclusive group for --function and --binary
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--function', help='Path to a decompiled C file for analysis')
    group.add_argument('--binary', help='Path to binary to produce function name map from')

    args = parser.parse_args()

    return args


def entry():
    args = parse_args()

    # compare a decompiled function with vectors
    if args.function:
        tweezer = Tweezer(args.model_path)
        tweezer.find_closest_functions(args.function)

    # Build a reference map of all functions in a binary
    elif args.binary:
        function_map = {}
        tweezer = Tweezer(args.model_path)
        with tempfile.TemporaryDirectory() as tmpdirname:
            g_bridge = GhidraBridge()
            g_bridge.decompile_binaries_functions(args.binary, tmpdirname)

            for file_path in Path(tmpdirname).iterdir():
                binary_name, function_name, *epoc = Path(file_path).name.split("__")
                closest_function = tweezer.find_closest_functions(args.function,1)
                function_map[function_name] = closest_function

        pprint(function_map)

    # Train / re train the model
    elif args.binary_locations:
        list_of_binary_folders = args.binary_locations
        tweezer = Tweezer(args.model_path)
        tweezer.setup_model(list_of_binary_folders)


if __name__ == '__main__':
    entry()
