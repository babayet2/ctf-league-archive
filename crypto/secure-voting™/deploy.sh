#!/bin/bash

set -e

./setup.py
docker-compose build
docker-compose up
