import configparser

# Reading the configuration file
config = configparser.ConfigParser()
config.read("app/config.ini")

# Defining configuration settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
JWT_TIMEOUT = int(config["jwt"]["timeout"])
