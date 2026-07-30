"""Utility helpers for scene generation."""


def format_scene(scene):
    """Return a simple text representation of a scene."""
    title = scene.get("title", "Untitled")
    content = scene.get("content", "")
    return f"{title}: {content}"
