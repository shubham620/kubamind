"""
Configuration module for KubeMind AI Backend
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Basic
    APP_NAME: str = "KubeMind AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "kubemind"
    POSTGRES_USER: str = "kubemind_user"
    POSTGRES_PASSWORD: str = "kubemind_password"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Vector Database
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: Optional[str] = None

    # Kubernetes
    KUBECONFIG_PATH: Optional[str] = None
    K8S_NAMESPACE: str = "default"

    # Prometheus
    PROMETHEUS_URL: str = "http://localhost:9090"
    PROMETHEUS_QUERY_TIMEOUT: int = 30

    # Loki
    LOKI_URL: str = "http://localhost:3100"

    # AI/LLM
    LLM_MODEL: str = "llama2"
    OLLAMA_URL: str = "http://localhost:11434"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Thresholds
    CPU_THRESHOLD_HIGH: float = 80.0
    CPU_THRESHOLD_CRITICAL: float = 95.0
    MEMORY_THRESHOLD_HIGH: float = 75.0
    MEMORY_THRESHOLD_CRITICAL: float = 90.0
    DISK_THRESHOLD_HIGH: float = 80.0
    DISK_THRESHOLD_CRITICAL: float = 95.0

    # Logging
    LOG_LEVEL: str = "INFO"

    # Feature Flags
    ENABLE_PREDICTIONS: bool = True
    ENABLE_CHAT_ASSISTANT: bool = True
    ENABLE_FAILURE_SIMULATION: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
