"""Static-scan fixture only; this module is never executed."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def encrypt_short_lived_internal_log_line(log_line: bytes) -> bytes:
    """Illustrate RSA encryption for a short-lived internal log line."""
    # Intended role: encryption; short-lived logs are low sensitivity (1-year lifetime).
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key.public_key().encrypt(
        log_line,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
