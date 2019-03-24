#!/usr/bin/env python3

import sys
import requests
import json
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

def error(msg):
    json.dump({"error": msg}, sys.stdout)
    sys.exit(1)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <url>", file=sys.stderr)
    sys.exit(0)

url = sys.argv[1]

try:
    resp = requests.get(url)
    resp.raise_for_status()
except requests.HTTPError:
    error(f"Could not load crl from {url}")

crl_data = resp.content
try:
    crl = x509.load_pem_x509_crl(crl_data, default_backend())
except ValueError:
    error(f"Could not parse CRL found at {url}")

crl_info = {
    "issuer": crl.issuer.rfc4514_string(),
    "last_update": crl.last_update.strftime("%s"),
    "next_update": crl.next_update.strftime("%s")
}

json.dump(crl_info, sys.stdout)
