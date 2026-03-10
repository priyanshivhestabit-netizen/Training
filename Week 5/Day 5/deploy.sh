#!/bin/bash

echo "Stopping old containers..."

docker compose -f docker-compose.yml down

echo "Building new images..."

docker compose -f docker-compose.yml build

echo "Starting production stack..."

docker compose -f docker-compose.yml up -d

echo "Deployment completed "