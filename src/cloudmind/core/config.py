"""Core configuration management for CloudMind AI."""

import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application
    app_name: str = "CloudMind AI"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, validation_alias="DEBUG")
    
    # API
    api_host: str = Field(default="0.0.0.0", validation_alias="API_HOST")
    api_port: int = Field(default=8000, validation_alias="API_PORT")
    api_reload: bool = Field(default=False, validation_alias="API_RELOAD")
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = Field(default=None, validation_alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, validation_alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(default="us-east-1", validation_alias="AWS_REGION")
    aws_enabled: bool = Field(default=False, validation_alias="AWS_ENABLED")
    
    # Azure Configuration
    azure_subscription_id: Optional[str] = Field(default=None, validation_alias="AZURE_SUBSCRIPTION_ID")
    azure_tenant_id: Optional[str] = Field(default=None, validation_alias="AZURE_TENANT_ID")
    azure_client_id: Optional[str] = Field(default=None, validation_alias="AZURE_CLIENT_ID")
    azure_client_secret: Optional[str] = Field(default=None, validation_alias="AZURE_CLIENT_SECRET")
    azure_enabled: bool = Field(default=False, validation_alias="AZURE_ENABLED")
    
    # Google Cloud Configuration
    gcp_project_id: Optional[str] = Field(default=None, validation_alias="GCP_PROJECT_ID")
    gcp_credentials_path: Optional[str] = Field(default=None, validation_alias="GCP_CREDENTIALS_PATH")
    gcp_enabled: bool = Field(default=False, validation_alias="GCP_ENABLED")
    
    # On-Premises Configuration
    onprem_enabled: bool = Field(default=False, validation_alias="ONPREM_ENABLED")
    onprem_hosts: List[str] = Field(default_factory=list, validation_alias="ONPREM_HOSTS")
    
    # AI/ML Configuration
    openai_api_key: Optional[str] = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", validation_alias="OPENAI_MODEL")
    ai_enabled: bool = Field(default=False, validation_alias="AI_ENABLED")
    
    # Monitoring
    monitoring_interval: int = Field(default=300, validation_alias="MONITORING_INTERVAL")  # 5 minutes
    alert_threshold_cpu: float = Field(default=80.0, validation_alias="ALERT_THRESHOLD_CPU")
    alert_threshold_memory: float = Field(default=80.0, validation_alias="ALERT_THRESHOLD_MEMORY")
    alert_threshold_cost: float = Field(default=1000.0, validation_alias="ALERT_THRESHOLD_COST")
    
    # Optimization
    auto_optimize: bool = Field(default=False, validation_alias="AUTO_OPTIMIZE")
    optimization_interval: int = Field(default=3600, validation_alias="OPTIMIZATION_INTERVAL")  # 1 hour
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
