#!/bin/bash

gunicorn --workers 4 main:app --bind 0.0.0.0:5000