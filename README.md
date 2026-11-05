# Hosted Helixor Solver starter

Clone this project, add the API origin and bearer token issued for your account, then run the same sample in Python or Node.js. It looks up the deployed `container_logistics` manifest, submits one small request, saves the complete response to `solve-result.json`, and checks the final feasibility evidence.

This starter calls the documented hosted REST API directly. The released solver contract SDK is currently consumed by Helixor's internal Decision Runtime integration; there is no published general-purpose Python or npm solver SDK documented for external developers. The project therefore does not pretend to install an SDK that users cannot obtain. The API contract and sample are linked below.

## What you need from your service owner

Ask your Helixor Solver administrator or service operator for:

1. The **Solver API origin** for your account and environment. It is the API service address, which may differ from the browser console URL.
2. A **bearer token** authorized to read manifests and submit solves for your tenant. Use the platform's approved sign-in and token issuance path. This starter does not collect your username or password and does not mint credentials.
3. Confirmation that the selected deployment includes the `container_logistics` manifest.

Hosted access uses the platform bearer token. This starter has no solver license-file step and does not download or decrypt local solver binaries. A customer-operated or embedded solver is a separate installation path; use the artifacts and license instructions supplied for that distribution.

Never commit `.env`, put tokens in browser code, or paste a token into a support issue. A `401` means the token was rejected; a `403` means the caller is not allowed to use that operation. Ask the service owner to check the token's audience, issuer, environment and grants. Do not disable authentication to work around either response.

## 1. Clone and configure

```bash
git clone https://github.com/HelixorAI/helixor-solver-starter.git
cd helixor-solver-starter
cp .env.example .env
```

Edit `.env` with the two values from your service owner:

```dotenv
SOLVER_URL=https://your-approved-solver-api-origin
SOLVER_TOKEN=your-issued-bearer-token
```

The committed example uses synthetic container and shipment records. Replace the records in `data/container-logistics-request.json` with your own data after the sample runs. Keep its `problem_type`, `problem`, and `solver` request shape, and validate your fields against the deployed manifest before relying on the result.

## 2. Run with Python

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
set -a && . ./.env && set +a    # Windows PowerShell: Get-Content .env | ForEach-Object { $name, $value = $_ -split '=', 2; Set-Item -Path "Env:$name" -Value $value }
python src/python/solve.py
```

The script uses `httpx`, gets the current manifest, sends the JSON request, prints the returned result and saves it to `solve-result.json`. It exits unsuccessfully on an HTTP error or when the final response lacks `solution.admission.is_feasible: true`.

## 3. Run with Node.js

Requires Node.js 20 or newer. The example uses the built-in `fetch`; no generated SDK is needed.

```bash
npm run solve
```

Node's `--env-file` option loads the same `.env`. The script performs the same manifest lookup, solve request and final-evidence check as the Python version.

## 4. Understand the response

The example is small: shipment `S1` can fit in container `C1`. Read the assignments and the returned admission evidence; an HTTP `200` alone does not establish that the final plan is feasible. The saved request and response are useful when debugging. Remove or redact business-sensitive data before sharing them.

To confirm the API refuses an incomplete request, copy the sample and set its `problem` to `{}`. The service should return its typed missing-input error. Do not treat a failed preflight, an exhausted search, or a transport error as a proof that the business problem is infeasible.

## Project layout

```text
.
├── .env.example
├── data/
│   └── container-logistics-request.json
├── src/
│   ├── node/solve.mjs
│   └── python/solve.py
├── package.json
└── requirements.txt
```

## Next steps

- [First hosted solve tutorial](https://helixor.dev/solver/tutorial/first-hosted-solve-a-complete.html)
- [Hosted API and request reference](https://helixor.dev/solver/reference/http-api.html)
- [Manifest authoring format](https://helixor.dev/solver/reference/manifest-format.html)
- [Container logistics manifest](https://helixor.dev/solver/problem-types/container-logistics.html)

The API origin, access grants, available problem types and credential issuance are deployment-specific. The tutorial's packaged sample is not a service availability guarantee.
