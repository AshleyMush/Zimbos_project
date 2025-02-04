import uuid

def generate_token():
    """Generates a unique token string using UUID."""
    return str(uuid.uuid4())
