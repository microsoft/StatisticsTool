from flask import Flask

from experiments_handlers.ExperminetsManager import ExperimentsManager

server = Flask(__name__)
experiments_manager = ExperimentsManager()
