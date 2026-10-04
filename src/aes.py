"""Static-scan AES fixtures only; zero-filled byte widths are placeholders, not keys."""

from cryptography.hazmat.primitives.ciphers.algorithms import AES


def use_aes_128_placeholder_key():
    """Intended role: encryption; 16 placeholder bytes represent a 128-bit key width."""
    return AES(bytes(16))


def use_aes_256_placeholder_key():
    """Intended role: encryption; 32 placeholder bytes represent a 256-bit key width."""
    return AES(bytes(32))
