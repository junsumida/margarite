#!/bin/sh

pkill -f 'gunicorn'
gunicorn -c gunicorn.py margarite:app