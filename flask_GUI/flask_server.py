from flask import Flask

from classes_and_utils.experiments.ExperminetsManager import ExperimentsManager

server = Flask(__name__)
experiments_manager = ExperimentsManager()
