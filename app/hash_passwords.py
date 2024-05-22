from passlib.context import CryptContext

# Creating a password context with bcrypt hashing scheme using Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a given password and return the hashed password


def get_password_hash(password):
    return pwd_context.hash(password)


# Dictionary containing username and password pairs to be hashed
users = {
    "testuser": "testpassword"
}

# Generating and printing the hashed password for each username and password pair
for username, password in users.items():
    hashed_password = get_password_hash(password)
    print(f"{username}:{hashed_password}")
