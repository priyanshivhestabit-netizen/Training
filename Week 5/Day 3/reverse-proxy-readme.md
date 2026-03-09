# Reverse Proxy with NGINX

NGINX is used as a reverse proxy to route requests to backend containers.

Architecture:

Browser → NGINX → Backend Containers

Two backend replicas are running:
- backend1
- backend2

Load balancing strategy:
Round Robin

Endpoint:
http://localhost:8080/api

Each request is forwarded to different backend container.