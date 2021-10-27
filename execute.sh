#!/bin/bash

URL="https://www.zoopla.co.uk/for-sale/property/golders-green/"
eval "./virtualenv/bin/python3 ./src/execute.py -u=\"$URL\""