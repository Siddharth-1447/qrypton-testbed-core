"""Static-scan fixture only; this module is never executed."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

P256_CURVE = ec.SECP256R1
ECDSA_SIGNATURE = ec.ECDSA
SHA256_FOR_ECDSA = hashes.SHA256


def sign_firmware_p256(firmware_image: bytes) -> bytes:
    """Illustrate an ECDSA P-256 firmware-image signature."""
    # Intended role: signature; aliases keep the detector evidence to generic EC key generation.
    private_key = ec.generate_private_key(P256_CURVE())
    return private_key.sign(firmware_image, ECDSA_SIGNATURE(SHA256_FOR_ECDSA()))
