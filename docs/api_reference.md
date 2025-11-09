# CloudMind AI - API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, CloudMind AI does not implement authentication for the API. In a production environment, you should implement proper authentication mechanisms such as API keys, OAuth, or JWT tokens.

## Endpoints

### Health & Status

#### GET /

Get API information and status.

**Response:**
```json
{
  "name": "CloudMind AI",
  "version": "0.1.0",
  "status": "running",
  "providers": ["aws", "azure", "gcp"],
  "ai_enabled": true
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "providers": {
    "aws": "connected",
    "azure": "connected"
  }
}
```

### Providers

#### GET /providers

List all configured cloud providers.

**Response:**
```json
{
  "providers": [
    {
      "name": "aws",
      "type": "aws",
      "status": "connected"
    }
  ]
}
```

### Resources

#### GET /resources/compute

List compute resources across providers.

**Query Parameters:**
- `provider` (optional): Filter by provider (aws, azure, gcp, onprem)
- `region` (optional): Filter by region

**Response:**
```json
{
  "count": 10,
  "resources": [
    {
      "id": "i-1234567890abcdef0",
      "name": "web-server-01",
      "provider": "aws",
      "resource_type": "compute",
      "status": "running",
      "region": "us-east-1",
      "created_at": "2024-01-01T00:00:00Z",
      "tags": {},
      "metadata": {},
      "instance_type": "t3.medium",
      "cpu_cores": 2,
      "memory_gb": 4.0
    }
  ]
}
```

#### GET /resources/storage

List storage resources across providers.

**Query Parameters:**
- `provider` (optional): Filter by provider
- `region` (optional): Filter by region

**Response:**
```json
{
  "count": 5,
  "resources": [
    {
      "id": "bucket-name",
      "name": "my-storage-bucket",
      "provider": "aws",
      "resource_type": "storage",
      "status": "running",
      "region": "us-east-1",
      "storage_type": "s3",
      "size_gb": 100.0
    }
  ]
}
```

#### GET /resources/database

List database resources across providers.

**Query Parameters:**
- `provider` (optional): Filter by provider
- `region` (optional): Filter by region

**Response:**
```json
{
  "count": 3,
  "resources": [
    {
      "id": "db-instance-1",
      "name": "production-db",
      "provider": "aws",
      "resource_type": "database",
      "status": "running",
      "region": "us-east-1",
      "database_type": "rds",
      "engine": "postgres",
      "version": "14.0",
      "size_gb": 500.0
    }
  ]
}
```

#### GET /resources/{resource_id}/metrics

Get current metrics for a specific resource.

**Query Parameters:**
- `provider` (required): Cloud provider name

**Response:**
```json
{
  "cpu_usage": 45.5,
  "memory_usage": 60.2,
  "network_in": 100.5,
  "network_out": 50.3
}
```

### Cost Management

#### GET /cost

Get cost data across all providers.

**Query Parameters:**
- `provider` (optional): Filter by specific provider

**Response:**
```json
{
  "count": 15,
  "total_daily_cost": 150.50,
  "total_monthly_cost": 4515.00,
  "costs": [
    {
      "resource_id": "i-1234567890abcdef0",
      "provider": "aws",
      "daily_cost": 10.50,
      "monthly_cost": 315.00,
      "currency": "USD",
      "last_updated": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Optimization

#### GET /optimization/recommendations

Get AI-powered optimization recommendations.

**Response:**
```json
{
  "summary": {
    "total_recommendations": 5,
    "total_estimated_savings": 250.50,
    "action_breakdown": {
      "downsize": 3,
      "stop": 2
    },
    "generated_at": "2024-01-15T10:30:00Z"
  },
  "recommendations": [
    {
      "resource_id": "i-1234567890abcdef0",
      "resource_name": "web-server-01",
      "provider": "aws",
      "action": "downsize",
      "reason": "Low CPU utilization detected (< 20%). Consider downsizing.",
      "estimated_savings": 50.00,
      "confidence": 0.85
    }
  ]
}
```

### Resource Management

#### POST /resources/{resource_id}/stop

Stop a running resource.

**Query Parameters:**
- `provider` (required): Cloud provider name

**Response:**
```json
{
  "success": true,
  "resource_id": "i-1234567890abcdef0",
  "action": "stop"
}
```

#### POST /resources/{resource_id}/start

Start a stopped resource.

**Query Parameters:**
- `provider` (required): Cloud provider name

**Response:**
```json
{
  "success": true,
  "resource_id": "i-1234567890abcdef0",
  "action": "start"
}
```

#### POST /resources/{resource_id}/resize

Resize a resource to a new instance type/size.

**Query Parameters:**
- `provider` (required): Cloud provider name
- `new_size` (required): New instance type/size

**Response:**
```json
{
  "success": true,
  "resource_id": "i-1234567890abcdef0",
  "action": "resize",
  "new_size": "t3.small"
}
```

#### DELETE /resources/{resource_id}

Delete a resource.

**Query Parameters:**
- `provider` (required): Cloud provider name

**Response:**
```json
{
  "success": true,
  "resource_id": "i-1234567890abcdef0",
  "action": "delete"
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK`: Successful request
- `404 Not Found`: Resource or provider not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service (e.g., AI) not enabled

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## CORS

CORS is enabled for all origins by default. In production, configure appropriate CORS policies.

## Interactive Documentation

CloudMind AI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test API endpoints directly from your browser.
