#!/usr/bin/env python3

import json
import sys

items = []

if len(sys.argv) > 1 and sys.argv[1] == "-":
    items = sys.stdin.read().strip().split("\n")
    sys.argv.pop(0)

items.extend(sys.argv[1:])

data = {}
for item in items:
    if "," not in item:
        print("Value '{}' does not contain a ','".format(item), file=sys.stderr)
        sys.exit(1)

    key, val = item.split(",", 1)
    data[key] = val

print(json.dumps(data))

