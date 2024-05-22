import os
from passlib.context import CryptContext

# Using Passlib for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify a plain password against a hashed password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a plain password


def get_password_hash(password):
    return pwd_context.hash(password)

# Function to read user data from a file


def read_users_from_file(file_path):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            username, password = line.strip().split(':')
            users[username] = password
    return users


# Load user data
users = read_users_from_file("app/user_data.txt")
