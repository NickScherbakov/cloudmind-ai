# CloudMind AI - Quick Start Guide

This guide will help you get CloudMind AI up and running in less than 5 minutes!

## 🚀 One-Click Installation

### For Testing and Demo

The fastest way to try CloudMind AI:

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/cloudmind-ai.git
cd cloudmind-ai

# Run the interactive setup
chmod +x setup.sh
./setup.sh
```

Select option **1** (Production mode) when prompted. The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs

### For Development

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/cloudmind-ai.git
cd cloudmind-ai

# Run setup and select option 2 (Development mode)
chmod +x setup.sh
./setup.sh
```

Or use Make:

```bash
make setup
make dev
```

Your changes to the `src/` directory will automatically trigger a reload.

## 📋 Prerequisites

You only need:
- **Docker** (20.10+) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (2.0+) - Usually included with Docker Desktop

That's it! All Python dependencies are handled automatically inside the container.

## 🎯 What's Next?

### 1. Configure Cloud Providers

Edit the `.env` file to add your cloud provider credentials:

```bash
# AWS
AWS_ENABLED=true
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# Azure
AZURE_ENABLED=true
AZURE_SUBSCRIPTION_ID=your_id
# ... other Azure settings
```

Restart the service after editing:

```bash
docker compose restart
# or
make restart
```

### 2. Try the API

Open your browser and go to http://localhost:8000/docs for interactive API documentation.

Try some endpoints:
- `GET /` - API information
- `GET /health` - Health check
- `GET /providers` - List configured cloud providers

### 3. Use the CLI

```bash
# Inside the container
docker compose exec cloudmind-api python cloudmind_cli.py --help

# One-off commands
docker compose run --rm cloudmind-api python cloudmind_cli.py version
docker compose run --rm cloudmind-api python cloudmind_cli.py info
```

### 4. Run Tests

```bash
docker compose -f docker-compose.dev.yml run --rm cloudmind-test
# or
make test
```

## 🔧 Common Commands

| Command | Description |
|---------|-------------|
| `./setup.sh` | Interactive setup menu |
| `make help` | Show all available commands |
| `make up` | Start in production mode |
| `make dev` | Start in development mode |
| `make test` | Run tests |
| `make logs` | View logs |
| `make stop` | Stop all services |
| `make clean` | Remove containers and images |

## 🆘 Troubleshooting

### Port 8000 is already in use

Edit `docker-compose.yml` and change the port mapping:

```yaml
ports:
  - "8001:8000"  # Use 8001 on your machine
```

### Changes not taking effect

If you modified the code and don't see changes:

1. Make sure you're using development mode: `make dev`
2. Check that files are being mounted: `docker compose -f docker-compose.dev.yml config`
3. Restart: `make restart`

### Can't connect to Docker

Make sure Docker is running:

```bash
docker ps
```

If it fails, start Docker Desktop (macOS/Windows) or run `sudo systemctl start docker` (Linux).

### Need help?

- Check the [Docker Setup Guide](docs/docker_setup.md) for detailed information
- See the main [README](../README.md) for API documentation
- Open an issue on GitHub

## 📚 Additional Resources

- [Full Documentation](../README.md)
- [Docker Setup Guide](docs/docker_setup.md)
- [API Reference](docs/api_reference.md)
- [Getting Started Guide](docs/getting_started.md)

## 💡 Tips for Contributors

1. Always use development mode when coding: `make dev`
2. Run tests before committing: `make test`
3. Check logs if something goes wrong: `make logs-dev`
4. Open a shell in the container for debugging: `make shell`

Happy coding! 🎉
