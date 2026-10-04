"""Placeholder RSA vector metadata and usage for static scanning; never execute."""

from cryptography.hazmat.primitives.asymmetric import rsa

RSA_VECTOR = {
    "algorithm": "RSA",
    "key_size_bits": 2048,
    "message_hex": "00",  # Non-secret placeholder; not a real test vector.
}


def generate_placeholder_rsa_vector_key():
    """Intended role: vector/test RSA use; this call is scan evidence, not test setup."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)
