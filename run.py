# run.py — production entrypoint referenced by Procfile.
#
# Bind to 0.0.0.0 (not uvicorn's default 127.0.0.1) so Knative's
# queue-proxy sidecar can reach the app across the pod-local loopback.
# Read the port from $PORT (Paketo + Knative convention), falling back
# to 8080 for local dev where PORT usually isn't set.
#
# Historic bug: previous version was
#   os.system("uvicorn app.main:app --reload")
# which (a) ignored any Procfile args passed to run.py because os.system
# starts a fresh subprocess, (b) defaulted to 127.0.0.1:8000, (c) ran
# in --reload dev mode. Result: Knative queue-proxy couldn't reach the
# app on localhost:8080, readiness probe timed out for 10+ min,
# ksvc never became Ready. Every new user following cli-quickstart.md
# to deploy this demo hit that wall.

import os
import sys

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Use os.execvp so uvicorn becomes PID 1 in the container — signals
    # (SIGTERM from Knative on scale-down) reach it directly instead of
    # dying at the shell wrapper.
    os.execvp("uvicorn", [
        "uvicorn", "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(port),
    ])
