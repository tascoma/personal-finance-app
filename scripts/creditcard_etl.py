import os
import configparser
import pandas as pd

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "../docs/config.ini")

config.read(config_path)
BANK_DIRECTORY = config.get('input_data_directory', 'BANK_DIRECTORY')
