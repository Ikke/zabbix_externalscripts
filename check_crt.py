#!/usr/bin/env python3
import sys
import time
import datetime
import subprocess
import io
import json
from datetime import datetime as dt


if len(sys.argv) < 2:
    print("Usage: ", sys.argv[0], " <domain>")
    sys.exit(1)

domain = sys.argv[1]

if not domain:
    print("Usage: ", sys.argv[0], " <domain>")
    sys.exit(1)

cert = io.StringIO()
found_cert = False

result = subprocess.run(
    "openssl s_client -connect {0}:443 -servername {0}".format(domain).split(" "),
    stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    encoding='utf-8')

for line in result.stdout.split("\n"):
    if "-----END CERTIFICATE-----" in line:
        cert.write(line + "\n")
        break
    elif "-----BEGIN CERTIFICATE-----" in line:
        found_cert = True
        cert.write(line + "\n")
    elif found_cert == True:
        cert.write(line + "\n")

if found_cert == False or not cert.getvalue().strip():
    print(0)
    sys.exit(0)

result = subprocess.run(
    "openssl x509 -noout -enddate".split(" "),
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    encoding='utf-8',
    input=cert.getvalue())

end_date = result.stdout.strip().split("=")[1]
# Mar 20 20:44:00 2016 GMT
delta = dt.strptime(end_date, "%b %d %H:%M:%S %Y %Z") - dt.utcnow()

output = {"days_left": delta.days, "hours_left": delta.days * 24 + delta.seconds // 3600, "end_date": end_date}
print(json.dumps(output))

