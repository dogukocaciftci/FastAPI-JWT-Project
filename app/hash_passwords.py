from passlib.context import CryptContext

# Passlib kullanarak bcrypt şifreleme şeması ile bir şifreleme bağlamı oluşturma
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verilen şifreyi hashleyip döndüren fonksiyon


def get_password_hash(password):
    return pwd_context.hash(password)


# Hashlenecek kullanıcı adı ve şifre çiftlerini içeren sözlük
users = {
    "testuser": "testpassword"
}

# Her kullanıcı adı ve şifre çifti için hashlenmiş şifreyi oluşturup yazdırma
for username, password in users.items():
    hashed_password = get_password_hash(password)
    print(f"{username}:{hashed_password}")
