"""Static-scanner fixture, not a behavioral test; do not execute this module."""

from cryptography.hazmat.primitives.asymmetric import rsa


def test_rsa_2048_call_for_static_scan():
    """Intended role: test-only RSA use; this function exists solely as scan input."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)
