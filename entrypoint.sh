#!/bin/sh
sleep 10
gunicorn app:app --bind 0.0.0.0:5000