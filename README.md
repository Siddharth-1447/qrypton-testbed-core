# qrypton-testbed-core

A small, inert source tree for checking QRYPTON scanner/risk-engine behavior against known expected findings. It contains placeholders only: no secrets, real keys, network calls, or credentials. **Do not run these fixtures**; they are static-analysis inputs. In particular, `tests/test_rsa.py` is deliberately a scanner fixture, not a behavioral pytest test.

The repository was created as a sibling of the QRYPTON checkout, not inside it. `expected_results.json` is the machine-readable contract; [`EXPECTED_RESULTS.md`](EXPECTED_RESULTS.md) explains detector evidence, constraints, contexts, and limitations.

## Included source fixtures

- `src/payment_gateway/tls.py` — RSA-2048 generation, intended TLS/key-exchange context.
- `src/firmware/sign.py` — P-256 EC key generation and ECDSA signing call.
- `src/internal_logging/crypto.py` — RSA use in an intended short-lived internal-log encryption context.
- `src/hashes.py` — separate MD5, SHA-1, SHA-256 calls.
- `src/aes.py` — AES constructor calls with 16-/32-byte zero placeholders.
- `src/pq.py` — ML-KEM-768 using the documented `pqcrypto.kem.ml_kem_768.keygen` API.
- `tests/test_rsa.py`, `tests/vectors/rsa_vectors.py` — path-class test/vector cases.

The inspected QRYPTON detector sees generic `ec` rather than ECDSA, and generic `aes` rather than AES key sizes. These limits are reflected rather than hidden in the expected results. `pqcrypto` is not a configured Python crypto-library prefix, but the ML-KEM call is recognized through the imported module path. See [PQCrypto's API](https://pypi.org/project/pqcrypto/).

## Push to GitHub (not performed)

Create an empty GitHub repository named `qrypton-testbed-core` (private is recommended), then from this directory run:

```powershell
cd "C:\New folder\Desktop\qrypton-testbed-core"
git remote add origin https://github.com/<YOUR_GITHUB_USER>/qrypton-testbed-core.git
git push -u origin main
```

Replace `<YOUR_GITHUB_USER>` with your GitHub account/organization. The local initial commit is already created; no remote was configured and nothing was pushed for this task.

## Scan from the QRYPTON dashboard

1. Push the repository using the commands above, then open the QRYPTON dashboard and authenticate.
2. Start **New scan** and select **Source repository**.
3. Enter `https://github.com/<YOUR_GITHUB_USER>/qrypton-testbed-core` as the locator and `main` as the branch/version tag.
4. Set Environment, Business criticality, X (data lifetime), Y (migration time), and Z (CRQC horizon), review, and start the scan. Use the scenario values in `EXPECTED_RESULTS.md` and set Y/Z intentionally; the inspected UI defaults (Y=4, Z=8) are not supplied by the test request.
5. Compare the algorithm-use findings and risk constraints against `expected_results.json`. Do not expect function comments alone to establish a crypto role.

### Dashboard caveats from the inspected local UI source

- The source-repository workflow asks for a URL and branch; it does not expose local-folder scanning.
- One context is submitted for the whole scan, so the dashboard cannot apply separate payment-gateway, firmware, and internal-logging contexts to different paths in this one repository scan.
- The current form has no internet-facing, data-sensitivity, or firmware-trust-lifetime fields. Business criticality and X are only proxies for those concepts; do not treat them as equivalent.
- The form displays a branch field, but the inspected page submission payload omits it. `main` is the documented default-like choice; verify the deployed dashboard/backend behavior if you use another branch.

No package install, crypto operation, or test execution is required for static scanning.
