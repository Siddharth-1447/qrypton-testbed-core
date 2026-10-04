"""Static-scan hashing fixtures only; this module is never executed."""

import hashlib


def hash_placeholder_md5(data: bytes) -> bytes:
    """Intended role: hashing; MD5 is present only as a scanner test primitive."""
    return hashlib.md5(data).digest()


def hash_placeholder_sha1(data: bytes) -> bytes:
    """Intended role: hashing; SHA-1 is present only as a scanner test primitive."""
    return hashlib.sha1(data).digest()


def hash_placeholder_sha256(data: bytes) -> bytes:
    """Intended role: hashing; SHA-256 is present only as a scanner test primitive."""
    return hashlib.sha256(data).digest()
