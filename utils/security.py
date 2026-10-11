import hashlib
import hmac
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    iterations = 100000
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations)
    return f"pbkdf2_sha256${iterations}${salt}${key.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    if not stored_hash or not password:
        return False

    parts = stored_hash.split("$")
    if len(parts) == 4 and parts[0] == "pbkdf2_sha256":
        _, iters, salt, key_hex = parts
        try:
            computed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iters))
            return hmac.compare_digest(computed.hex(), key_hex)
        except (ValueError, TypeError):
            return False

    # Fallback comparison for legacy plaintext entries
    return hmac.compare_digest(password, stored_hash)

