FROM nginx:1.25-alpine

# Install required packages
RUN apk add --no-cache curl openssl

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Create necessary directories
RUN mkdir -p /var/www/certbot /var/www/html /var/log/nginx

# Copy nginx configuration templates
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Copy entrypoint script for environment variable substitution
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create custom error pages
RUN echo '<html><body><h1>Service Temporarily Unavailable</h1></body></html>' > /var/www/html/50x.html

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

EXPOSE 80 443

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]