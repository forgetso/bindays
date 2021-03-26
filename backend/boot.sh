#!/bin/sh
exec waitress-serve --port=5000 api:app