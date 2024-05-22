import configparser

# Konfigürasyon dosyasını okuma
config = configparser.ConfigParser()
config.read("app/config.ini")

# Konfigürasyon ayarlarını tanımlama
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
JWT_TIMEOUT = int(config["jwt"]["timeout"])
