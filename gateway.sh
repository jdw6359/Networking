#!/bin/bash

ip route | head -n1 | awk '{print $3}'
