#!/bin/bash

# Run the application in a local docker container

set -e

docker run \
       --env FLASK_ENV=development \
       --env OPENAI_API_KEY=$OPENAI_API_KEY \
       -p 3000:3000 \
       -it \
       hackathon-field-analysis
