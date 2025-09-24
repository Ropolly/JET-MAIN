#!/bin/sh
if [ -f "/etc/nginx/ssl/live/${NGINX_HOST}/fullchain.pem" ]; then
    echo "SSL certificates found, using HTTPS configuration"
    cp /etc/nginx/conf.d/ssl.conf /etc/nginx/conf.d/default.conf
else
    echo "No SSL certificates found, using HTTP configuration"
    cp /etc/nginx/conf.d/nginx.conf /etc/nginx/conf.d/default.conf
    rm -f /etc/nginx/conf.d/ssl.conf
fi
exec "$@"
