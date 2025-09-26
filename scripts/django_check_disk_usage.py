#!/usr/bin/python

import argparse
import json
import sys

from urllib.request import urlopen

import six

CRITICAL = 90
WARNING = 80

parser = argparse.ArgumentParser(description='Checks disk usage on remote host.')

parser.add_argument('url', help='URL of remote endpoint.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

max_percentage = 0
max_device = None

for device, percentage in list(data.items()):
    if percentage > max_percentage:
        max_percentage = percentage
        max_device = device

if max_device is None:
    six.print_('DISK UNKNOWN: ' + args.url)
    sys.exit(3)
elif max_percentage >= CRITICAL:
    six.print_('DISK CRITICAL: ' + max_device + ', ' + str(max_percentage) + '%')
    sys.exit(2)
elif max_percentage >= WARNING:
    six.print_('DISK CRITICAL: ' + max_device + ', ' + str(max_percentage) + '%')
    sys.exit(2)
else:
    six.print_('DISK OK: ' + max_device + ', ' + str(max_percentage) + '%')
    sys.exit(0)
