from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, Dict, Any, List
from enums import BasicStatus

class LibraryBase(BaseModel):
    name: str
    api_endpoint: str
    docker_image: Optional[str] = None
    docker_tag: Optional[str] = "latest"
    api_key: Optional[str] = None
    api_headers: Optional[Dict[str, str]] = None
    timeout_seconds: Optional[int] = 30
    retry_count: Optional[int] = 3
    docker_env_vars: Optional[Dict[str, str]] = None
    docker_ports: Optional[Dict[str, int]] = None  # {"container_port": host_port}
    docker_volumes: Optional[Dict[str, str]] = None  # {"host_path": "container_path"}
    health_check_endpoint: Optional[str] = None
    description: Optional[str] = None
    status: BasicStatus

class LibraryCreate(LibraryBase):
    pass

class LibraryUpdate(BaseModel):
    name: Optional[str] = None
    api_endpoint: Optional[str] = None
    docker_image: Optional[str] = None
    docker_tag: Optional[str] = None
    api_key: Optional[str] = None
    api_headers: Optional[Dict[str, str]] = None
    timeout_seconds: Optional[int] = None
    retry_count: Optional[int] = None
    docker_env_vars: Optional[Dict[str, str]] = None
    docker_ports: Optional[Dict[str, int]] = None
    docker_volumes: Optional[Dict[str, str]] = None
    health_check_endpoint: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BasicStatus] = None

class Library(LibraryBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
