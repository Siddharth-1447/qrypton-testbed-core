# Expected scanner results

This manifest is a **test contract for the source scanner**, not a promise about exact dashboard tier labels. Each item identifies the intended primitive and the detector evidence that should appear. Behavior constraints are risk-engine assertions; the local source detector itself only emits source observations.

## Scanner capabilities confirmed from the QRYPTON checkout

Inspected the local scanner implementation at `C:\New folder\Desktop\qrypton\src\qrypton\scanners\source\` (especially `rules.py`, `python_ast.py`, `cpp_lexical.py`, `scanner.py`, `traversal.py`, and `policy.py`). No QRYPTON files were changed.

- **Languages/extensions:** Python (`.py`), C (`.c`, `.h`), and C++ (`.cc`, `.cpp`, `.cxx`, `.hh`, `.hpp`). Python uses an import-bound AST detector; C/C++ uses a bounded lexical detector with recognized API-name prefixes. JavaScript/TypeScript, Java, Go, Rust, and other extensions are not selected by this source scanner.
- **Python matching:** an algorithm-like call must resolve through an import to a dotted name containing a token in the scanner's algorithm catalog. Comments and strings do not trigger algorithm-call findings. Recognized catalog includes MD5, SHA-1/224/256/384/512, SHA3-256, AES, ChaCha20, RSA, EC, DSA, DH, X25519/X448, Ed25519/Ed448, HMAC, HKDF, PBKDF2, scrypt, Argon2, ML-KEM, ML-DSA, and SLH-DSA. This is a catalog, not a claim that every arbitrary spelling/API is detected.
- **Detected API shapes used here:** `hashlib.md5/sha1/sha256(...)`; `rsa.generate_private_key(..., key_size=2048)`; `ec.generate_private_key(P256_CURVE())` where `P256_CURVE = ec.SECP256R1`; imported `AES(...)`; and `keygen()` imported from `pqcrypto.kem.ml_kem_768`. RSA's literal `key_size` is captured as a parameter. AES positional key bytes are not converted into key-size metadata.
- **C/C++ prefixes:** `EVP_aes`, `AES_`, `EVP_sha`, `SHA`, `MD5`, `RSA_`, `EVP_PKEY_RSA`, `EVP_PKEY_EC`, `crypto_box`, `crypto_sign`, `BCrypt`, `CCCrypt`, `mbedtls_aes`, `mbedtls_sha`, and `wolfSSL`; header corroboration recognizes `openssl/`, `mbedtls/`, `wolfssl/`, sodium, bcrypt, and CommonCrypto. This repository intentionally uses Python only.

## Known non-detections and closest supported patterns

1. **ECDSA as a distinct signature primitive: not detected.** There is no `ecdsa` rule. The firmware fixture uses aliases for `SECP256R1`, `ECDSA`, and `SHA256`, so only `ec.generate_private_key(P256_CURVE())` is detected as generic `ec`; the aliased ECDSA and variable-bound `.sign(...)` calls are not algorithm matches. The manifest does not claim the scanner proved the signature operation.
2. **AES-128 versus AES-256: not distinguished.** Both constructors produce generic `aes`. The placeholder byte widths are visible to a human but the AST detector does not derive `key_size_bits` from positional arguments. Do not expect two different scanner algorithm names or key-size metadata.
3. **RSA role/linkage: not inferred.** `rsa.generate_private_key(..., key_size=2048)` is detected as `rsa` with 2048 bits, but comments/function names do not prove TLS key exchange or log encryption. The chained `.public_key().encrypt(...)` call is not independently classified as RSA encryption. TLS context detection is separate from RSA attribution.
4. **Path class/context: not assigned by the source detector.** It reports the relative path. Production/test/vector classification and test/vector caps must be applied by the risk policy, not assumed to come from this detector.
5. **PQC import nuance:** `pqcrypto` is not one of the scanner's listed Python crypto-library prefixes, so this should produce algorithm evidence via the imported module path and `keygen()` call, not library-import evidence. The module/API is documented by [PQCrypto on PyPI](https://pypi.org/project/pqcrypto/); its current catalog includes `ml_kem_768` and the KEM API uses `keygen`/`encaps`/`decaps`.

## Business contexts to enter or approximate in the dashboard

| Target | Intended context | Dashboard mapping / limitation |
|---|---|---|
| `payment_gateway` | Production; internet-facing; high sensitivity; data lifetime X = 20 years | Set Environment = Production, Business criticality = High (only a proxy, not sensitivity), X = 20. The inspected form has no internet-facing or sensitivity field. Its displayed defaults are Y = 4 and Z = 8 years; verify/set the values you intend rather than treating defaults as user requirements. |
| `firmware` | Trust lifetime = 15 years | X = 15 is only a proxy for the firmware trust lifetime; the form calls X “Data lifetime” and has no trust-lifetime control. Environment/criticality were not specified. Y/Z are not specified; the UI snapshot defaults to 4/8. |
| `internal_logging` | Low sensitivity; data lifetime X = 1 year | Set Business criticality = Low only as a proxy; the form has no sensitivity field. Environment was not specified. Y/Z are not specified; the UI snapshot defaults to 4/8. |

The inspected dashboard scan form takes one context for a source-repository scan, not separate contexts for `payment_gateway`, `firmware`, and `internal_logging`. Consequently, per-directory comparisons require a path-aware capability or separate scoped targets/fixtures; a single whole-repository scan cannot faithfully apply all three contexts at once. These UI facts are based on `web/src/components/scan-workflow.tsx` and the submission payload in `web/src/app/page.tsx` from the inspected local checkout.

## Expected algorithm-use findings

| File | Function | Primitive / detector result | Class | Role | Path class | Trigger |
|---|---|---|---|---|---|---|
| `src/payment_gateway/tls.py` | `generate_tls_rsa_2048_key_exchange` | RSA-2048 / generic `rsa`, 2048-bit parameter | `SHOR_VULNERABLE` | Intended TLS key exchange | production | `rsa.generate_private_key(public_exponent=65537, key_size=2048)` |
| `src/firmware/sign.py` | `sign_firmware_p256` | Intended ECDSA P-256 / generic `ec` only | `SHOR_VULNERABLE` | Firmware signature | production | `ec.generate_private_key(P256_CURVE())` with module alias `P256_CURVE = ec.SECP256R1` |
| `src/internal_logging/crypto.py` | `encrypt_short_lived_internal_log_line` | RSA-2048 / generic `rsa`, 2048-bit parameter | `SHOR_VULNERABLE` | Intended short-lived log encryption | production | `rsa.generate_private_key(public_exponent=65537, key_size=2048)` |
| `src/hashes.py` | `hash_placeholder_md5` | MD5 / `md5` | `CLASSICALLY_WEAK` | Hashing | production | `hashlib.md5(data)` |
| `src/hashes.py` | `hash_placeholder_sha1` | SHA-1 / `sha-1` | `CLASSICALLY_WEAK` | Hashing | production | `hashlib.sha1(data)` |
| `src/hashes.py` | `hash_placeholder_sha256` | SHA-256 / `sha-256` | `GROVER_REDUCED` | Hashing | production | `hashlib.sha256(data)` |
| `src/aes.py` | `use_aes_128_placeholder_key` | Intended AES-128 / generic `aes`; size unavailable | `GROVER_REDUCED` | Encryption | production | `AES(bytes(16))` |
| `src/aes.py` | `use_aes_256_placeholder_key` | Intended AES-256 / generic `aes`; size unavailable | `GROVER_REDUCED` | Encryption | production | `AES(bytes(32))` |
| `src/pq.py` | `generate_ml_kem_768_placeholder_keypair` | ML-KEM-768 / `ml-kem` | `POST_QUANTUM` | Key encapsulation | production | `keygen()` imported from `pqcrypto.kem.ml_kem_768` |
| `tests/test_rsa.py` | `test_rsa_2048_call_for_static_scan` | RSA-2048 / generic `rsa`, 2048-bit parameter | `SHOR_VULNERABLE` | Test-only use | test | `rsa.generate_private_key(public_exponent=65537, key_size=2048)` |
| `tests/vectors/rsa_vectors.py` | `generate_placeholder_rsa_vector_key` | RSA-2048 / generic `rsa`, 2048-bit parameter | `SHOR_VULNERABLE` | Vector/test use | vector | `rsa.generate_private_key(public_exponent=65537, key_size=2048)` |

The complete per-finding machine-readable contract, including all required fields and constraints, is in [`expected_results.json`](expected_results.json).

## Behavior constraints

- Production RSA/EC quantum exposure **must depend on Z**; it may become critical only when the configured exposure/business model supports that outcome. The 20-year payment context should rank above the 1-year low-sensitivity internal-logging context for the same RSA primitive.
- MD5/SHA-1 are **classically weak now**, so their weakness must not depend on Z. For the same role/context, MD5 should not rank below SHA-1, and both should rank above SHA-256.
- SHA-256 and AES are subject to Grover-style reduction, not Shor breakage. The fixtures expect `GROVER_REDUCED`, and the engine must not treat Grover reduction alone as equivalent to a Shor-vulnerable RSA/EC finding. AES-128/AES-256 relative ordering is not testable from this scanner's generic AES evidence.
- ML-KEM is `POST_QUANTUM` and must not be classified as Shor-vulnerable legacy public-key crypto solely because it is a KEM.
- Same-primitive production use should outrank test/vector use; test/vector findings **must be capped at low** and never be critical. The local scanner does not implement that path-aware risk behavior, so this is an expected risk-engine policy constraint, not scanner output.
- `must_never_be_critical: true` means **not critical solely on the basis of the stated quantum effect**; unrelated business or policy factors may still independently raise risk. Exact levels are intentionally omitted because tier labels/configuration can vary.
