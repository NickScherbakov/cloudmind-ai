#!/usr/bin/env python3
"""Entry point for CloudMind AI API server."""

import uvicorn
from cloudmind.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "cloudmind.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
