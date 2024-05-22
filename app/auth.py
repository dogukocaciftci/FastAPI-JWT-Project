import os
from passlib.context import CryptContext

# Şifreleme için Passlib kullanımı
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Şifre doğrulama fonksiyonu


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Şifre hashleme fonksiyonu


def get_password_hash(password):
    return pwd_context.hash(password)

# Kullanıcı verilerini dosyadan okuma fonksiyonu


def read_users_from_file(file_path):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            username, password = line.strip().split(':')
            users[username] = password
    return users


# Kullanıcı verilerini yükleme
users = read_users_from_file("app/user_data.txt")
