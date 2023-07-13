#!/bin/bash

## compile front-end code into bundle
npx webpack --config config/webpack.config.js

## start flask server on port 5000
gunicorn --config config/gunicorn.conf.py --chdir src/server/ server:app
