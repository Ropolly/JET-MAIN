# Production Dockerfile for Vue frontend
FROM node:18-alpine as builder

# Set build arguments
ARG VITE_APP_API_URL=/api

# Install dependencies for building
RUN apk add --no-cache python3 make g++

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including devDependencies for build)
RUN npm ci

# Copy all frontend files
COPY . .

# Set build-time environment variables
ENV VITE_APP_API_URL=$VITE_APP_API_URL

# Build the Vue application (this will now work with the fixed FBOs.vue)
RUN npm run build

# Production stage - Nginx
FROM nginx:alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Remove default nginx config
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy nginx configurations
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
COPY nginx-ssl.conf /etc/nginx/conf.d/ssl.conf

# Copy custom entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create directory for Let's Encrypt challenges
RUN mkdir -p /var/www/certbot

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Create a non-root user to run nginx
RUN addgroup -g 101 -S nginx && \
    adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx || true

# Set correct permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Use entrypoint to configure SSL dynamically
ENTRYPOINT ["/docker-entrypoint.sh"]

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
