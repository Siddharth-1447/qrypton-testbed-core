"""Static-scan fixture only; this module is never executed."""

from cryptography.hazmat.primitives.asymmetric import rsa


def generate_tls_rsa_2048_key_exchange():
    """RSA-2048 key-generation marker for the payment gateway TLS role."""
    # Intended role: key exchange for an internet-facing TLS endpoint.
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)
