# CloudMind AI Production Deployment Guide

This guide covers deploying CloudMind AI to production environments.

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- Server with at least 2GB RAM and 10GB disk space
- Valid cloud provider credentials
- (Optional) Domain name and SSL certificate

## Quick Production Deployment

### 1. Prepare the Server

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/cloudmind-ai.git
cd cloudmind-ai

# Create production .env file
cp .env.example .env
nano .env  # Edit with your credentials
```

### 3. Configure Environment

Edit `.env` with production settings:

```env
# Application Settings
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# Enable Cloud Providers
AWS_ENABLED=true
AWS_ACCESS_KEY_ID=your_production_key
AWS_SECRET_ACCESS_KEY=your_production_secret
AWS_REGION=us-east-1

# Enable AI Features
AI_ENABLED=true
OPENAI_API_KEY=your_production_key
OPENAI_MODEL=gpt-4

# Production Monitoring
MONITORING_INTERVAL=300
ALERT_THRESHOLD_CPU=80.0
ALERT_THRESHOLD_MEMORY=80.0
ALERT_THRESHOLD_COST=1000.0

# Optimization Settings
AUTO_OPTIMIZE=false  # Set to true for automatic optimization
OPTIMIZATION_INTERVAL=3600
```

### 4. Deploy

```bash
# Start in production mode
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### 5. Verify Deployment

```bash
# Check health
curl http://localhost:8000/health

# Check API documentation
curl http://localhost:8000/docs
```

## Security Hardening

### 1. Network Security

**Use a reverse proxy (Nginx):**

```nginx
server {
    listen 80;
    server_name cloudmind.example.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable SSL with Let's Encrypt:**

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d cloudmind.example.com
```

### 2. Firewall Configuration

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### 3. Container Security

Update `docker-compose.yml` with security options:

```yaml
services:
  cloudmind-api:
    # ... existing config ...
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 4. Environment Variables

Never commit `.env` to version control. Use secrets management:

```bash
# Using Docker Secrets (Swarm mode)
echo "your_secret" | docker secret create openai_key -

# Update docker-compose.yml to use secrets
secrets:
  openai_key:
    external: true
```

## High Availability Setup

### Docker Swarm Deployment

```bash
# Initialize Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml cloudmind

# Scale services
docker service scale cloudmind_cloudmind-api=3
```

### Load Balancer Configuration

Example with Traefik:

```yaml
services:
  traefik:
    image: traefik:v2.9
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
  
  cloudmind-api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.cloudmind.rule=Host(`cloudmind.example.com`)"
```

## Monitoring and Logging

### 1. Container Logs

```bash
# View logs
docker compose logs -f

# Export logs to file
docker compose logs > cloudmind.log

# Rotate logs
docker compose logs --tail=1000 > cloudmind-$(date +%Y%m%d).log
```

### 2. Application Monitoring

Add Prometheus monitoring (optional):

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### 3. Health Checks

The container includes built-in health checks. Monitor them:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' cloudmind-api

# Set up external monitoring (example with uptime checker)
curl -s http://your-server:8000/health | jq .status
```

## Backup and Recovery

### 1. Backup Configuration

```bash
# Backup .env and credentials
tar -czf cloudmind-config-$(date +%Y%m%d).tar.gz .env credentials/

# Backup to remote location
scp cloudmind-config-*.tar.gz user@backup-server:/backups/
```

### 2. Container State Backup

```bash
# Export container
docker commit cloudmind-api cloudmind-backup:$(date +%Y%m%d)

# Save image
docker save cloudmind-backup:$(date +%Y%m%d) | gzip > cloudmind-backup-$(date +%Y%m%d).tar.gz
```

### 3. Disaster Recovery

```bash
# Stop services
docker compose down

# Restore configuration
tar -xzf cloudmind-config-YYYYMMDD.tar.gz

# Rebuild and start
docker compose up -d --build
```

## Updates and Maintenance

### Rolling Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild with zero downtime
docker compose up -d --build --no-deps cloudmind-api

# Verify
docker compose ps
```

### Scheduled Maintenance

Create a cron job for regular maintenance:

```bash
# Edit crontab
crontab -e

# Add maintenance tasks
0 2 * * 0 cd /path/to/cloudmind-ai && docker compose down && docker system prune -af && docker compose up -d
```

## Performance Optimization

### 1. Resource Limits

Update `docker-compose.yml`:

```yaml
services:
  cloudmind-api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### 2. Caching

Enable Docker BuildKit for faster builds:

```bash
export DOCKER_BUILDKIT=1
docker compose build
```

### 3. Volume Optimization

Use named volumes for better performance:

```yaml
volumes:
  cloudmind-data:
    driver: local
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs

# Check resource usage
docker stats

# Verify .env file
cat .env | grep -v "PASSWORD\|SECRET\|KEY"
```

### High Memory Usage

```bash
# Check container stats
docker stats cloudmind-api

# Restart container
docker compose restart
```

### Network Issues

```bash
# Check container network
docker network inspect cloudmind-network

# Restart networking
docker compose down && docker compose up -d
```

## Production Checklist

Before going live:

- [ ] All secrets configured in .env
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Backup system in place
- [ ] Monitoring configured
- [ ] Health checks working
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Rollback plan prepared
- [ ] Team notified

## Support

For production issues:

1. Check logs: `docker compose logs -f`
2. Verify configuration: `docker compose config`
3. Review health status: `curl http://localhost:8000/health`
4. Open an issue on GitHub with details

## Additional Resources

- [Docker Setup Guide](docker_setup.md)
- [Quick Start Guide](../QUICKSTART.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Main README](../README.md)
