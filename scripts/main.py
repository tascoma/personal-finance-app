import os
import configparser
import scripts
from paystub_etl import paystub_etl
from creditcard_etl import creditcard_etl


cwd = os.path.dirname(__file__)

# Initializing Configuration
config = configparser.ConfigParser()
config_path = os.path.join(cwd, "../docs/config.ini")
config.read(config_path)


def main():
    paystub_etl(cwd, config)
    creditcard_etl(cwd, config)


if __name__ == "__main__":
    main()
