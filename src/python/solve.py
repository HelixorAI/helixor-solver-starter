"""Submit the bundled sample request to a hosted Helixor Solver API."""
from __future__ import annotations

import json
import os
from pathlib import Path

import httpx


def main() -> int:
    base_url = os.environ["SOLVER_URL"].rstrip("/")
    token = os.environ["SOLVER_TOKEN"]
    request = json.loads(Path("data/container-logistics-request.json").read_text())
    problem_type = request["problem_type"]

    with httpx.Client(timeout=60) as client:
        manifest_response = client.get(
            f"{base_url}/api/v1/manifests/{problem_type}",
            headers={"Authorization": f"Bearer {token}"},
        )
        if not manifest_response.is_success:
            print(f"Manifest lookup failed ({manifest_response.status_code}): {manifest_response.text}")
            return 1
        manifest = manifest_response.json()
        print(f"Using manifest: {manifest.get('problem_type', problem_type)}")

        response = client.post(
            f"{base_url}/api/v1/solve/{problem_type}",
            headers={"Authorization": f"Bearer {token}"},
            json=request,
        )
        if not response.is_success:
            print(f"Solve failed ({response.status_code}): {response.text}")
            return 1
        result = response.json()

    Path("solve-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    admission = (result.get("solution") or {}).get("admission") or {}
    if admission.get("is_feasible") is not True:
        print("The API returned, but the final plan did not carry feasible admission evidence.")
        return 2
    print("Final plan includes feasibility evidence.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyError as exc:
        raise SystemExit(f"Missing required environment value: {exc.args[0]}. Copy .env.example to .env and fill it in.")
    except httpx.RequestError as exc:
        raise SystemExit(f"Could not reach the configured solver API: {exc}")
