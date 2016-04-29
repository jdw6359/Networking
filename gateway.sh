#!/bin/bash

echo "running ip route script"

ip route | head -n1 | awk '{print $3}'

echo "done running ip route script"
