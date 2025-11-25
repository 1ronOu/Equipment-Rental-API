import bcrypt




def hash_password(
        password: str,
):
    salt = bcrypt.gensalt()
    pdw_bytes: bytes = password.encode()
    return bcrypt.hashpw(pdw_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes,
):
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )


