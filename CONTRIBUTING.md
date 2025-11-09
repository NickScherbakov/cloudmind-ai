# Contributing to CloudMind AI

Thank you for your interest in contributing to CloudMind AI! This guide will help you get started with development.

## 🚀 Quick Start for Contributors

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/cloudmind-ai.git
cd cloudmind-ai

# Add upstream remote
git remote add upstream https://github.com/NickScherbakov/cloudmind-ai.git
```

### 2. Set Up Development Environment

**Using Docker (Recommended):**

```bash
# Start development environment with hot-reload
make setup
make dev
```

Your changes will automatically trigger a reload. The API will be available at http://localhost:8000.

**Without Docker (Alternative):**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH=src:$PYTHONPATH  # On Windows: set PYTHONPATH=src;%PYTHONPATH%

# Run the API
python cloudmind_api.py
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

Edit the code in the `src/` directory. If using Docker development mode, changes will auto-reload.

### 5. Test Your Changes

```bash
# Run tests
make test
# or without Docker
PYTHONPATH=src pytest tests/ -v

# Test the API manually
curl http://localhost:8000/health
```

### 6. Commit and Push

```bash
git add .
git commit -m "Description of your changes"
git push origin feature/your-feature-name
```

### 7. Create Pull Request

Go to GitHub and create a Pull Request from your branch to the main repository.

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Project Structure

```
cloudmind-ai/
├── src/cloudmind/         # Main application code
│   ├── core/              # Core functionality
│   ├── providers/         # Cloud provider implementations
│   ├── ai/                # AI/ML services
│   ├── monitoring/        # Monitoring services
│   ├── api/               # FastAPI endpoints
│   └── cli/               # CLI commands
├── tests/                 # Test files
├── docs/                  # Documentation
└── examples/              # Example scripts
```

### Adding a New Feature

1. **Create a new branch**: `git checkout -b feature/feature-name`
2. **Write tests first**: Add tests in `tests/` directory
3. **Implement the feature**: Add code in appropriate module
4. **Update documentation**: Add/update docs in `docs/` directory
5. **Test thoroughly**: Run all tests and manual testing
6. **Submit PR**: Create a pull request with description

### Adding a New Cloud Provider

To add support for a new cloud provider:

1. Create a new file in `src/cloudmind/providers/` (e.g., `new_provider.py`)
2. Inherit from `CloudProviderBase`
3. Implement all abstract methods
4. Add configuration in `src/cloudmind/core/config.py`
5. Update `.env.example` with new provider settings
6. Add tests in `tests/unit/test_providers.py`
7. Update documentation

Example:

```python
from cloudmind.providers.base import CloudProviderBase

class NewCloudProvider(CloudProviderBase):
    def authenticate(self) -> bool:
        # Implementation
        pass
    
    def list_compute_resources(self) -> List[ComputeResource]:
        # Implementation
        pass
    
    # ... other required methods
```

### Testing

**Run all tests:**
```bash
make test
```

**Run specific test file:**
```bash
PYTHONPATH=src pytest tests/unit/test_api.py -v
```

**Run tests with coverage:**
```bash
PYTHONPATH=src pytest --cov=cloudmind tests/
```

### Docker Development Tips

**Access container shell:**
```bash
make shell
```

**View logs:**
```bash
make logs-dev
```

**Restart after config changes:**
```bash
make restart
```

**Rebuild after dependency changes:**
```bash
make build
make dev
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Docker version, Python version)
6. Relevant logs or error messages

## 💡 Suggesting Features

We welcome feature suggestions! Please:

1. Check if the feature is already requested
2. Describe the use case clearly
3. Explain the expected behavior
4. Provide examples if possible

## 📝 Documentation

When updating documentation:

- Use clear, concise language
- Include code examples
- Update the relevant `.md` files in `docs/`
- Keep the main `README.md` updated

## ✅ Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] Tests are added/updated and passing
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main branch
- [ ] No merge conflicts
- [ ] Docker builds successfully
- [ ] CI/CD checks pass

## 🔄 Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream main into your local main
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## 🎯 Good First Issues

Look for issues labeled `good first issue` to start contributing. These are typically:

- Documentation improvements
- Simple bug fixes
- Adding tests
- Code cleanup

## 💬 Communication

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Pull Requests**: For code contributions

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow project guidelines

## 🙏 Thank You!

Your contributions make CloudMind AI better for everyone. Thank you for taking the time to contribute!

## 📚 Additional Resources

- [Quick Start Guide](QUICKSTART.md)
- [Docker Setup Guide](docs/docker_setup.md)
- [API Reference](docs/api_reference.md)
- [Getting Started](docs/getting_started.md)
