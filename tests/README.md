# CloudMind AI - Tests

This directory contains the test suite for CloudMind AI.

## Test Structure

```
tests/
├── unit/              # Unit tests for individual modules
│   ├── test_config.py
│   ├── test_models.py
│   ├── test_providers.py
│   ├── test_ai_optimizer.py
│   └── test_utils.py
└── integration/       # Integration tests (to be added)
```

## Running Tests

### Run all tests

```bash
PYTHONPATH=src pytest tests/
```

### Run only unit tests

```bash
PYTHONPATH=src pytest tests/unit/ -v
```

### Run specific test file

```bash
PYTHONPATH=src pytest tests/unit/test_config.py -v
```

### Run specific test

```bash
PYTHONPATH=src pytest tests/unit/test_config.py::test_settings_default_values -v
```

### Run with coverage

```bash
PYTHONPATH=src pytest tests/ --cov=cloudmind --cov-report=html
```

## Test Coverage

Current test coverage includes:

- ✅ Core configuration management
- ✅ Data models and validation
- ✅ Provider factory
- ✅ AI optimization service
- ✅ Utility functions

## Writing Tests

When adding new tests:

1. Place unit tests in `tests/unit/`
2. Place integration tests in `tests/integration/`
3. Follow the naming convention: `test_*.py`
4. Use pytest fixtures for reusable test data
5. Keep tests focused and independent

### Example Test

```python
import pytest
from cloudmind.core.models import CloudProvider

def test_cloud_provider_enum():
    """Test CloudProvider enum values."""
    assert CloudProvider.AWS.value == "aws"
    assert CloudProvider.AZURE.value == "azure"
```

## Dependencies

Tests require:
- pytest
- pytest-asyncio (for async tests)

Install with:
```bash
pip install pytest pytest-asyncio
```
