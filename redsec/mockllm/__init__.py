"""Deterministic, deliberately-vulnerable LLM used across the range."""
from .backends import Backend, MockBackend, OpenAICompatBackend, get_backend
from .engine import Completion, Engine, Message, Tool, ToolCall

__all__ = [
    "Backend",
    "MockBackend",
    "OpenAICompatBackend",
    "get_backend",
    "Completion",
    "Engine",
    "Message",
    "Tool",
    "ToolCall",
]
