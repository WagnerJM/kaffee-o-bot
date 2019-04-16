#!/bin/bash

# Create data folder in the current directory
echo "Creating data folder"

if [ ! -d data ]
then
  echo "data directory does not exists"
  mkdir -p ./data
  echo "Directory created"
else
  echo "Directory exists"
fi

 Create .env file in the root dir
if [ ! -f ./.env ]
then
  echo ".env file not found, creating new file ..."
  python ./server/app/utils/setup.py
else
  echo ".env already exists"
fi

# populate the .env file with environment variables

#python ./server/app/lib/setup.py
