# Transitions

This directory contains optional video transition effects that ClipForge AI can expose in the UI and use during video clip rendering.

## How it works

- Place `.mp4` video files into this directory.
- The backend automatically discovers available transitions via `GET /transitions`.
- Transitions can be applied between clips or used as cut transitions.

## Supported formats

- `.mp4`

## Adding transitions

1. Drop your `.mp4` transition files into this directory.
2. Restart the backend/worker containers if they do not appear immediately (`docker compose restart backend worker ai-worker`).
3. Verify they are available in the app or via `GET /transitions`.
