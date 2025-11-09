# CloudMind AI

Open source platform for automated management and optimization of cloud resources (AWS, Azure, Google Cloud, on-prem) using modern artificial intelligence models (LLM, ML).

## Features

### 🌩️ Multi-Cloud Support
- **AWS**: EC2, S3, RDS, Lambda, and more
- **Azure**: Virtual Machines, Storage, SQL Database
- **Google Cloud**: Compute Engine, Cloud Storage, Cloud SQL
- **On-Premises**: Monitor and manage on-prem infrastructure

### 🤖 AI-Powered Optimization
- Intelligent resource analysis using LLMs
- ML-based usage prediction
- Cost optimization recommendations
- Automated resource rightsizing

### 📊 Comprehensive Monitoring
- Real-time resource metrics collection
- Historical data tracking
- Custom alert configurations
- Health status assessments

### 🔧 Resource Management
- Start, stop, resize, and delete resources
- Cross-cloud resource inventory
- Cost tracking and analysis
- Automated optimization actions

### 🚀 Multiple Interfaces
- **REST API**: Full-featured FastAPI backend
- **CLI**: Rich command-line interface with Typer
- **Programmatic**: Python SDK for custom integrations

## Installation

### Prerequisites
- Python 3.8+
- pip or poetry

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Application
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000

# AWS Configuration
AWS_ENABLED=true
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Azure Configuration
AZURE_ENABLED=false
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# Google Cloud Configuration
GCP_ENABLED=false
GCP_PROJECT_ID=your_project_id
GCP_CREDENTIALS_PATH=/path/to/credentials.json

# On-Premises Configuration
ONPREM_ENABLED=false
ONPREM_HOSTS=host1.example.com,host2.example.com

# AI Configuration
AI_ENABLED=true
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# Monitoring
MONITORING_INTERVAL=300
ALERT_THRESHOLD_CPU=80.0
ALERT_THRESHOLD_MEMORY=80.0
ALERT_THRESHOLD_COST=1000.0

# Optimization
AUTO_OPTIMIZE=false
OPTIMIZATION_INTERVAL=3600
```

## Usage

### REST API

Start the API server:

```bash
python cloudmind_api.py
```

Or using uvicorn directly:

```bash
uvicorn cloudmind.api.main:app --host 0.0.0.0 --port 8000
```

Access the API documentation at: `http://localhost:8000/docs`

### CLI Commands

Show version:
```bash
python cloudmind_cli.py version
```

Show configuration:
```bash
python cloudmind_cli.py info
```

List resources:
```bash
python cloudmind_cli.py list-resources --provider aws --type compute
python cloudmind_cli.py list-resources --provider azure --type storage
```

Get resource metrics:
```bash
python cloudmind_cli.py get-metrics --provider aws --resource i-1234567890abcdef0
```

Get optimization recommendations:
```bash
python cloudmind_cli.py optimize
python cloudmind_cli.py optimize --provider aws
```

Manage resources:
```bash
python cloudmind_cli.py stop-resource --provider aws --resource i-1234567890abcdef0
python cloudmind_cli.py start-resource --provider aws --resource i-1234567890abcdef0
```

Start API from CLI:
```bash
python cloudmind_cli.py start-api --host 0.0.0.0 --port 8000
```

## API Endpoints

### General
- `GET /` - API information
- `GET /health` - Health check
- `GET /providers` - List configured providers

### Resources
- `GET /resources/compute` - List compute resources
- `GET /resources/storage` - List storage resources
- `GET /resources/database` - List database resources
- `GET /resources/{resource_id}/metrics` - Get resource metrics
- `POST /resources/{resource_id}/start` - Start a resource
- `POST /resources/{resource_id}/stop` - Stop a resource
- `POST /resources/{resource_id}/resize` - Resize a resource
- `DELETE /resources/{resource_id}` - Delete a resource

### Cost & Optimization
- `GET /cost` - Get cost data across providers
- `GET /optimization/recommendations` - Get AI-powered optimization recommendations

## Architecture

```
cloudmind-ai/
├── src/cloudmind/
│   ├── core/           # Core functionality (config, models, exceptions)
│   ├── providers/      # Cloud provider implementations
│   ├── ai/             # AI/ML optimization services
│   ├── monitoring/     # Resource monitoring services
│   ├── api/            # FastAPI REST API
│   ├── cli/            # Command-line interface
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Usage examples
```

## Development

### Project Structure

- **Core Module**: Configuration, logging, data models, and exceptions
- **Providers Module**: Abstract base class and implementations for each cloud provider
- **AI Module**: LLM integration and ML-based optimization algorithms
- **Monitoring Module**: Resource metrics collection and alerting
- **API Module**: FastAPI REST API with comprehensive endpoints
- **CLI Module**: Rich CLI interface with Typer

### Extending CloudMind AI

#### Adding a New Cloud Provider

1. Create a new provider class inheriting from `CloudProviderBase`
2. Implement all abstract methods
3. Register the provider in `ProviderFactory`

Example:
```python
from cloudmind.providers.base import CloudProviderBase

class MyCloudProvider(CloudProviderBase):
    def authenticate(self) -> bool:
        # Implementation
        pass
    
    # Implement other required methods...
```

#### Adding Custom Optimization Logic

Extend the `AIOptimizationService` class:
```python
from cloudmind.ai import AIOptimizationService

class CustomOptimizer(AIOptimizationService):
    def analyze_resource(self, resource, metrics, cost_data):
        # Custom logic
        pass
```

## Security

- Never commit API keys or credentials to version control
- Use environment variables for sensitive configuration
- Follow cloud provider security best practices
- Implement proper authentication for API endpoints in production

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] Enhanced ML models for usage prediction
- [ ] Advanced cost forecasting
- [ ] Multi-region optimization
- [ ] Automated policy enforcement
- [ ] Web dashboard UI
- [ ] Kubernetes integration
- [ ] Terraform integration
- [ ] Slack/Teams notifications
- [ ] Cost anomaly detection
- [ ] Compliance checking

## Support

For questions and support, please open an issue on GitHub.

## Acknowledgments

Built with modern Python frameworks:
- FastAPI for REST API
- Typer for CLI
- Pydantic for data validation
- Rich for beautiful terminal output
