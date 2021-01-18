import argparse, os
from loader import LoadModel
import pathlib
import json
import logging

logging.root.setLevel(logging.INFO)

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def dir_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid file")

def name_c(name):
    if '//ver/' in name:
        raise argparse.ArgumentTypeError(f"name:{name} contains '_ver/'. Use a different name.")
    else:
        return name


parser = argparse.ArgumentParser(
    description='Sets up an express Jaeger server.'
)

# needs a single model and name for startup.
parser.add_argument(
        "--file",
        metavar='AbsolutePath',
        type=lambda p: pathlib.Path(p).absolute(),
        help="Path to the data directory",
)
parser.add_argument('--name', type=name_c, metavar="String", help="Name for the model which will be used for the serving links. If not supplied, Name of the parent folder of model will be used.")
parser.add_argument('--model_conf', type=dir_file, metavar="AbsolutePath", help="Config file to specify multiple models.")
parser.add_argument('--port', metavar="PORT", help="The port for the server. Default is 8501.", default=8501)
parser.add_argument('--server', default="paste", help="The server that Bottle will run on. Default is Bjoern, for windows installations, choose 'paste' or any other server bottle supports.")
args = parser.parse_args()

if args.file and args.name:
    LoadModel(args.file, name=str(args.name))

if args.file and not args.name:
    LoadModel(args.file)


def get_from_config():
    if args.model_conf:
        with open(args.model_conf) as file:
            for line in file:
                line = line.strip().split(',')
                if line[0] == 'model':
                    name = line[1].strip()
                    if '//ver/' in name:
                        logging.error(f"Model name on {name} from the model config specified contains '//ver/'. Do not use '//ver/' on model names.")
                        raise ValueError(f"Model name on {name} from the model config specified contains '//ver/.' Do not use '//ver/' on model names.")
                    elif '/' in name:
                        logging.error(f"Model name on {name} from the model config specified contains '/'. Do not use '/' on model names as it conflicts with how URLs are read.")
                        raise ValueError(f"Model name on {name} from the model config specified contains '/'. Do not use '/' on model names as it conflicts with how URLs are read.")
                    path = line[2].strip()
                    LoadModel(pathlib.Path(path), name=name)


get_from_config()
print(LoadModel.modelsByName)
from server import *
try:
    logging.info(f"Starting server at 0.0.0.0:{args.port}")
    runserver(args.port, args.server)
except Exception as e:
    logging.error("W Exception while starting up server.", exc_info=True)
