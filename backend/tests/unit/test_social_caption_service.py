import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.services import social_caption_service as captions


async def test_caption_uses_haiku_and_grounded_clip_data(monkeypatch):
    run = AsyncMock(return_value=SimpleNamespace(output="  Watch this idea.  "))
    settings = {}

    def agent(model, **kwargs):
        settings.update(kwargs)
        settings["model"] = model.model_name
        return SimpleNamespace(run=run)

    monkeypatch.setattr(captions, "Agent", agent)
    result = await captions.generate_social_caption(
        "test-key", {"hook_title": "An idea", "text": "A real transcript"}, "instagram"
    )
    assert result == "Watch this idea."
    assert settings["model"] == "claude-haiku-5-5"
    assert "temperature" not in settings["model_settings"]
    assert json.loads(run.await_args.args[0]) == {
        "platform": "instagram", "headline": "An idea", "transcript": "A real transcript"
    }


@pytest.mark.parametrize("output", [" ", "x" * 2201])
async def test_rejects_invalid_caption(monkeypatch, output):
    monkeypatch.setattr(captions, "Agent", lambda *args, **kwargs: SimpleNamespace(
        run=AsyncMock(return_value=SimpleNamespace(output=output))
    ))
    with pytest.raises(ValueError):
        await captions.generate_social_caption("test-key", {"text": "Transcript"}, "youtube")


async def test_caption_uses_configured_google_gemini_without_anthropic_key(monkeypatch):
    from src.config import Config

    run = AsyncMock(return_value=SimpleNamespace(output="  Gemini caption  "))
    captured = {}

    def agent(model, **kwargs):
        captured["model"] = model
        return SimpleNamespace(run=run)

    cfg = Config()
    cfg.anthropic_api_key = None
    cfg.google_api_key = "fake-google-key"
    cfg.llm = "google-gla:gemini-2.5-flash"

    monkeypatch.setattr(captions, "Agent", agent)
    result = await captions.generate_social_caption(
        "", {"hook_title": "Hook", "text": "Transcript"}, "instagram", config=cfg
    )
    assert result == "Gemini caption"
    assert captured["model"] == "google-gla:gemini-2.5-flash"
