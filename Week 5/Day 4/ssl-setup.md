# SSL Setup

SSL enabled using mkcert.

Commands used:

mkcert -install
mkcert localhost

Certificates generated:

localhost.pem
localhost-key.pem

NGINX configured for HTTPS on port 443.

HTTP requests redirected to HTTPS.

Test URL:
https://localhost/api

