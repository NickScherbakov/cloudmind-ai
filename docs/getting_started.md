# CloudMind AI - Getting Started Guide

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Quick Start](#quick-start)
4. [Architecture Overview](#architecture-overview)
5. [Usage Examples](#usage-examples)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Cloud provider credentials (for at least one provider)

### Step 1: Clone the Repository

```bash
git clone https://github.com/NickScherbakov/cloudmind-ai.git
cd cloudmind-ai
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

### Environment Variables

CloudMind AI uses environment variables for configuration. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials and preferences.

### AWS Configuration

To enable AWS support:

1. Set `AWS_ENABLED=true`
2. Provide AWS credentials:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `AWS_REGION`: Default AWS region (e.g., us-east-1)

```env
AWS_ENABLED=true
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

### Azure Configuration

To enable Azure support:

1. Set `AZURE_ENABLED=true`
2. Provide Azure credentials:
   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID
   - `AZURE_TENANT_ID`: Your Azure tenant ID
   - `AZURE_CLIENT_ID`: Your Azure client/application ID
   - `AZURE_CLIENT_SECRET`: Your Azure client secret

### Google Cloud Configuration

To enable GCP support:

1. Set `GCP_ENABLED=true`
2. Provide GCP credentials:
   - `GCP_PROJECT_ID`: Your GCP project ID
   - `GCP_CREDENTIALS_PATH`: Path to your service account JSON file

### AI Configuration

To enable AI-powered optimization:

1. Set `AI_ENABLED=true`
2. Provide OpenAI API key:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: Model to use (default: gpt-4)

## Quick Start

### Using the REST API

1. Start the API server:

```bash
python cloudmind_api.py
```

2. Access the interactive API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Test the health endpoint:

```bash
curl http://localhost:8000/health
```

### Using the CLI

1. Show version information:

```bash
python cloudmind_cli.py version
```

2. List compute resources:

```bash
python cloudmind_cli.py list-resources --provider aws --type compute
```

3. Get optimization recommendations:

```bash
python cloudmind_cli.py optimize
```

### Using as a Python Library

```python
from cloudmind.core.config import settings
from cloudmind.core.models import CloudProvider
from cloudmind.providers import ProviderFactory

# Initialize provider
config = {
    "region": settings.aws_region,
    "access_key_id": settings.aws_access_key_id,
    "secret_access_key": settings.aws_secret_access_key,
}
provider = ProviderFactory.create_provider(CloudProvider.AWS, config)
provider.authenticate()

# List resources
resources = provider.list_compute_resources()
print(f"Found {len(resources)} resources")
```

## Architecture Overview

### Core Components

1. **Core Module** (`cloudmind/core/`)
   - Configuration management
   - Data models and schemas
   - Logging and error handling
   - Custom exceptions

2. **Providers Module** (`cloudmind/providers/`)
   - Abstract base interface
   - AWS implementation
   - Azure implementation
   - GCP implementation
   - On-premises implementation

3. **AI Module** (`cloudmind/ai/`)
   - LLM integration
   - Resource analysis
   - Optimization recommendations
   - Usage prediction

4. **Monitoring Module** (`cloudmind/monitoring/`)
   - Metrics collection
   - Alert management
   - Health assessments
   - Historical data tracking

5. **API Module** (`cloudmind/api/`)
   - FastAPI REST endpoints
   - Request/response handling
   - CORS configuration

6. **CLI Module** (`cloudmind/cli/`)
   - Typer command-line interface
   - Rich formatting
   - Interactive commands

### Data Flow

```
User Request → API/CLI → Provider Factory → Cloud Provider → Cloud API
                              ↓
                        Monitoring Service
                              ↓
                        AI Optimization Service
                              ↓
                        Recommendations/Actions
```

## Usage Examples

See the `examples/` directory for detailed usage examples:

- `basic_usage.py`: Basic programmatic usage
- `multi_cloud.py`: Working with multiple cloud providers

Run an example:

```bash
python examples/basic_usage.py
```

## Next Steps

- Configure your cloud providers in `.env`
- Explore the API documentation at `/docs`
- Try the CLI commands
- Check out the examples in `examples/`
- Read the API reference in `docs/api_reference.md`

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:
1. Verify your credentials in `.env`
2. Check that the provider is enabled
3. Ensure proper permissions are granted
4. Review the logs for detailed error messages

### No Resources Found

If no resources are returned:
1. Verify you have resources in the specified region
2. Check that your credentials have read permissions
3. Try listing resources in different regions
4. Use the cloud provider's console to verify resources exist

### API Connection Issues

If the API won't start:
1. Check that the port is not already in use
2. Verify all dependencies are installed
3. Review the startup logs for errors
4. Try a different port using `--port` option

## Support

For additional help:
- Review the full documentation in `docs/`
- Check GitHub issues
- Refer to the API documentation at `/docs`
