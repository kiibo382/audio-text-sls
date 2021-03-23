#!/bin/bash

aws s3 rm s3://sls-tutorial-dev-transcribe-bucket --recursive
npm run sls-remove