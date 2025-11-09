# Docker Setup Guide

This guide explains how to run CloudMind AI using Docker for easy one-click deployment and development.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

## Quick Start

### Option 1: Using the Setup Script (Recommended)

The easiest way to get started:

```bash
# Make the script executable
chmod +x setup.sh

# Run the interactive setup
./setup.sh
```

The script will guide you through:
1. Creating the `.env` configuration file
2. Starting in production or development mode
3. Running tests
4. Managing containers

### Option 2: Using Make Commands

If you have `make` installed:

```bash
# See all available commands
make help

# Initial setup
make setup

# Start in production mode
make build
make up

# Start in development mode (with hot-reload)
make dev

# Run tests
make test

# View logs
make logs

# Stop services
make stop
```

### Option 3: Using Docker Compose Directly

```bash
# Create .env file
cp .env.example .env

# Production mode
docker-compose up -d --build

# Development mode
docker-compose -f docker-compose.dev.yml up --build

# Run tests
docker-compose -f docker-compose.dev.yml run --rm cloudmind-test
```

## Deployment Modes

### Production Mode

Optimized for production deployment:
- Minimal image size with multi-stage build
- No hot-reload
- Better performance
- Read-only application code

```bash
docker-compose up -d
```

Access the API:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Development Mode

Optimized for development and contribution:
- Hot-reload enabled (changes to code trigger automatic restart)
- Source code mounted as volumes
- Development tools included
- Easy debugging

```bash
docker-compose -f docker-compose.dev.yml up
```

Changes to these files will trigger auto-reload:
- `src/` directory (all Python source code)
- `cloudmind_api.py`
- `cloudmind_cli.py`

### Test Mode

Run the test suite in an isolated container:

```bash
docker-compose -f docker-compose.dev.yml run --rm cloudmind-test
```

Or using make:

```bash
make test
```

## Configuration

### Environment Variables

Edit the `.env` file to configure CloudMind AI:

```env
# Application Settings
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000

# Cloud Provider Credentials
AWS_ENABLED=true
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# AI Configuration
AI_ENABLED=true
OPENAI_API_KEY=your_openai_key
```

### Cloud Provider Credentials

For cloud providers that require credential files (e.g., GCP):

1. Create a `credentials` directory in the project root
2. Place your credential files there
3. Reference them in `.env`:

```env
GCP_CREDENTIALS_PATH=/app/credentials/gcp-credentials.json
```

The `credentials` directory is mounted as read-only in the container.

## Container Management

### View Running Containers

```bash
docker-compose ps
# or
make ps
```

### View Logs

```bash
# Production logs
docker-compose logs -f
# or
make logs

# Development logs
docker-compose -f docker-compose.dev.yml logs -f
# or
make logs-dev
```

### Access Container Shell

```bash
# Development container
docker-compose -f docker-compose.dev.yml run --rm cloudmind-dev /bin/bash
# or
make shell

# Production container
docker-compose run --rm cloudmind-api /bin/bash
# or
make shell-prod
```

### Stop Services

```bash
# Stop all services
docker-compose down
docker-compose -f docker-compose.dev.yml down
# or
make stop
```

### Restart Services

```bash
docker-compose restart
# or
make restart
```

## Cleanup

### Remove Containers and Images

```bash
docker-compose down -v --rmi local
# or
make clean
```

### Complete Cleanup

To remove everything including images built by Docker Compose:

```bash
docker-compose down -v --rmi all
docker-compose -f docker-compose.dev.yml down -v --rmi all
```

## Using the CLI in Docker

### Interactive CLI

Access the CLI inside a running container:

```bash
docker-compose exec cloudmind-api python cloudmind_cli.py --help
```

### One-off CLI Commands

Run CLI commands without starting the full service:

```bash
# Production container
docker-compose run --rm cloudmind-api python cloudmind_cli.py version

# Development container
docker-compose -f docker-compose.dev.yml run --rm cloudmind-dev python cloudmind_cli.py info
```

Examples:

```bash
# Show version
docker-compose run --rm cloudmind-api python cloudmind_cli.py version

# List resources
docker-compose run --rm cloudmind-api python cloudmind_cli.py list-resources --provider aws

# Get optimization recommendations
docker-compose run --rm cloudmind-api python cloudmind_cli.py optimize
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change it in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Use port 8001 on host, 8000 in container
```

### Permission Issues

If you encounter permission issues with mounted volumes:

```bash
# Fix permissions
sudo chown -R $USER:$USER .
```

### Container Won't Start

Check the logs:

```bash
docker-compose logs
```

Verify the `.env` file exists and is properly configured:

```bash
cat .env
```

### Cannot Connect to Docker Daemon

Make sure Docker is running:

```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop
```

### Hot-Reload Not Working

Make sure you're using the development compose file:

```bash
docker-compose -f docker-compose.dev.yml up
```

## Advanced Usage

### Custom Docker Commands

You can customize the container behavior by editing:
- `Dockerfile` - Production image configuration
- `Dockerfile.dev` - Development image configuration
- `docker-compose.yml` - Production service configuration
- `docker-compose.dev.yml` - Development service configuration

### Network Configuration

Containers are connected via the `cloudmind-network` bridge network. To connect other services:

```yaml
services:
  your-service:
    networks:
      - cloudmind-network

networks:
  cloudmind-network:
    external: true
```

### Health Checks

The production container includes health checks:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' cloudmind-api
```

## CI/CD Integration

### Building Images

```bash
# Build production image
docker build -t cloudmind-ai:latest .

# Build development image
docker build -f Dockerfile.dev -t cloudmind-ai:dev .
```

### Running Tests in CI

```bash
# Run tests without interactive mode
docker-compose -f docker-compose.dev.yml run --rm cloudmind-test
```

## Performance Tips

### Production Optimization

1. Use production mode for deployment
2. Configure appropriate resource limits in `docker-compose.yml`
3. Use environment-specific `.env` files

### Development Optimization

1. Use development mode for coding
2. Mount only necessary directories
3. Use `.dockerignore` to exclude unnecessary files from the build context

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify your configuration: `cat .env`
3. Ensure all prerequisites are installed
4. Open an issue on GitHub with the error details
