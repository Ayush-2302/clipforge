"""
Configuration for the ClipForge AI MCP server.

All settings come from environment variables so the same server binary works
against the official hosted instance (the default) or any self-hosted backend.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

# The official hosted ClipForge AI API. Override with CLIPFORGE_API_URL to point at
# a self-hosted backend (e.g. http://localhost:8000).
DEFAULT_API_URL = "https://api.clipforge.ai"
# The web app: where users create API keys and pick a plan.
DEFAULT_APP_URL = "https://www.clipforge.ai"

# "http" serves Streamable HTTP at /mcp and legacy SSE at /sse from one
# process. "sse" and "streamable-http" are older names for the same thing.
HTTP_TRANSPORT_ALIASES = {"http", "sse", "streamable-http", "streamable_http", "both"}


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


@dataclass(frozen=True)
class Settings:
    """Resolved runtime configuration."""

    api_url: str
    api_key: Optional[str]
    user_id: Optional[str]
    auth_secret: Optional[str]
    download_dir: str
    timeout: float
    mcp_transport: str
    mcp_host: str
    mcp_port: int
    mcp_mount_path: str
    mcp_public_url: Optional[str]
    mcp_require_bearer_auth: bool
    app_url: str = DEFAULT_APP_URL
    # Shared with the backend. Set (with bearer auth on) to let connectors sign in with OAuth.
    mcp_oauth_secret: Optional[str] = None

    @property
    def oauth_enabled(self) -> bool:
        return bool(self.mcp_oauth_secret) and self.mcp_require_bearer_auth

    @property
    def auth_mode(self) -> str:
        """Describe how requests will be authenticated."""
        if self.api_key:
            return "api_key"
        if self.user_id and self.auth_secret:
            return "signed_headers"
        if self.user_id:
            return "unsigned_user_id"
        return "none"

    @property
    def is_authenticated(self) -> bool:
        return self.auth_mode != "none"


def _get(key: str) -> Optional[str]:
    return _clean(os.getenv(f"CLIPFORGE_{key}") or os.getenv(f"CLIPFORGE_{key}"))


def load_settings() -> Settings:
    """Build :class:`Settings` from the current environment."""
    api_url = (_get("API_URL") or DEFAULT_API_URL).rstrip("/")
    download_dir = _get("DOWNLOAD_DIR") or os.path.join(
        os.getcwd(), "clipforge-downloads"
    )

    raw_timeout = _get("TIMEOUT")
    try:
        timeout = float(raw_timeout) if raw_timeout else 60.0
    except ValueError:
        timeout = 60.0

    raw_port = _get("MCP_PORT")
    try:
        mcp_port = int(raw_port) if raw_port else 9100
    except ValueError:
        mcp_port = 9100

    transport = (_get("MCP_TRANSPORT") or "stdio").lower()
    transport = "http" if transport in HTTP_TRANSPORT_ALIASES else "stdio"

    return Settings(
        api_url=api_url,
        app_url=(_get("APP_URL") or DEFAULT_APP_URL).rstrip("/"),
        mcp_oauth_secret=_clean(os.getenv("MCP_OAUTH_SECRET")),
        api_key=_get("API_KEY"),
        user_id=_get("USER_ID"),
        auth_secret=_get("AUTH_SECRET"),
        download_dir=download_dir,
        timeout=timeout,
        mcp_transport=transport,
        mcp_host=_get("MCP_HOST") or "127.0.0.1",
        mcp_port=mcp_port,
        mcp_mount_path=_get("MCP_MOUNT_PATH") or "/",
        mcp_public_url=_get("MCP_PUBLIC_URL"),
        mcp_require_bearer_auth=(
            (_get("MCP_REQUIRE_BEARER_AUTH") or "").lower()
            in {"1", "true", "yes", "on"}
        ),
    )
