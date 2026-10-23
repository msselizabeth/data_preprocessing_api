import secrets
import hashlib

def generate_api_key() -> tuple[str, str]:
    key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(key.encode('utf-8'), usedforsecurity=True).hexdigest()
    return (key, key_hash)

# if __name__ == "__main__":
#     generate_api_key()