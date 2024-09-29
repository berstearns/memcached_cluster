#!/bin/bash

# Run Certbot to obtain a certificate
certbot --nginx -d bernardostearns.com -d www.bernardostearns.com --non-interactive --agree-tos --email berstearns@gmail.com

# Start Nginx
nginx -g 'daemon off;'
