#!/usr/bin/env python3

import json
import sys

data = {}
for item in sys.argv[1:]:
    key, val = item.split(",", 1)
    data[key] = val

print(json.dumps(data))

