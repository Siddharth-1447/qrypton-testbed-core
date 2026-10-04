"""Static-scan post-quantum fixture only; this module is never executed."""

from pqcrypto.kem.ml_kem_768 import keygen


def generate_ml_kem_768_placeholder_keypair():
    """Intended role: post-quantum key encapsulation; generated material is never used."""
    return keygen()
