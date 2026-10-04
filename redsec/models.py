"""Pydantic models for a RedSec module manifest (``module.yaml``).

A module is the unit of the framework: author a ``module.yaml`` + a vulnerable
target + a verifier, and the CLI/Helm can render it, deploy it, and check whether
the exploit worked. Everything about a module is declarative here so the
framework stays expandable without touching infrastructure code.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class Difficulty(str, Enum):
    intro = "intro"
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class Mappings(BaseModel):
    """Traceability to the taxonomies the course is built on."""

    ai300_module: int | None = Field(
        None, description="Corresponding OffSec AI-300 module number (1-11)."
    )
    owasp_llm: list[str] = Field(
        default_factory=list, description="OWASP LLM Top 10 IDs, e.g. LLM01."
    )
    owasp_mcp: list[str] = Field(
        default_factory=list, description="OWASP MCP Top 10 IDs."
    )
    mitre_atlas: list[str] = Field(
        default_factory=list, description="MITRE ATLAS technique IDs, e.g. AML.T0051."
    )


class NetworkPolicy(BaseModel):
    egress: bool = Field(
        False,
        description="Allow the target to reach the internet. Default-deny for "
        "safety and because egress isolation is itself a teaching point.",
    )
    allow_targets: list[str] = Field(
        default_factory=list,
        description="Names of sibling targets this target may reach "
        "(same range namespace). The shared 'drop' sink is always reachable.",
    )


class RunSpec(BaseModel):
    """How to run a target locally (no Docker needed) for `redsec dev`."""

    asgi: str | None = Field(
        None, description="ASGI app import path, e.g. 'app:app' (served by uvicorn)."
    )
    cmd: list[str] | None = Field(
        None, description="Explicit command (overrides asgi)."
    )
    cwd: str | None = Field(None, description="Working dir relative to target build dir.")


class Target(BaseModel):
    name: str
    kind: Literal["http", "mcp", "sink", "custom"] = "http"
    image: str | None = Field(
        None, description="Prebuilt image ref. If absent, build from `build`."
    )
    build: str | None = Field(
        None, description="Path (relative to module dir) containing a Dockerfile."
    )
    uses_builtin: str | None = Field(
        None, description="Name of a framework-provided target, e.g. 'drop'."
    )
    run: RunSpec | None = None
    port: int = 8000
    env: dict[str, str] = Field(default_factory=dict)
    privileged: bool = Field(
        False,
        description="Target intentionally runs with weak isolation (e.g. for an "
        "RCE challenge). Must be explicit; forces strict NetworkPolicy lockdown.",
    )
    network: NetworkPolicy = Field(default_factory=NetworkPolicy)

    @field_validator("name")
    @classmethod
    def _dns_safe(cls, v: str) -> str:
        if not v.replace("-", "").isalnum() or not v[0].isalpha():
            raise ValueError(f"target name {v!r} must be DNS-label safe")
        return v.lower()


class VerifyStep(BaseModel):
    type: Literal["flag", "oracle", "artifact"] = "flag"
    check: str | None = Field(
        None,
        description="'module:Class' dotted ref into the module's verify package, "
        "or a builtin name. Required for oracle/artifact; optional for flag.",
    )
    flag: str | None = Field(
        None, description="Expected flag for a simple 'flag' check (hash-compared)."
    )
    params: dict[str, Any] = Field(default_factory=dict)


class Challenge(BaseModel):
    id: str
    title: str
    objective: str = ""
    points: int = 100
    difficulty: Difficulty | None = None
    primitive: str | None = Field(
        None, description="For MCP module: the protocol primitive under attack."
    )
    verify: list[VerifyStep] = Field(default_factory=list)
    hints: list[str] = Field(default_factory=list)
    flag_format: str = "REDSEC{...}"

    @field_validator("id")
    @classmethod
    def _slug(cls, v: str) -> str:
        if not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError(f"challenge id {v!r} must be alphanumeric/-/_")
        return v


class Module(BaseModel):
    id: str = Field(description="Two-digit module id, e.g. '03'.")
    slug: str
    title: str
    summary: str = ""
    difficulty: Difficulty = Difficulty.intermediate
    estimated_minutes: int = 60
    status: Literal["complete", "scaffold", "draft"] = "scaffold"
    authors: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    mappings: Mappings = Field(default_factory=Mappings)
    targets: list[Target] = Field(default_factory=list)
    challenges: list[Challenge] = Field(default_factory=list)
    lesson: str = "lesson.md"

    @property
    def dirname(self) -> str:
        return f"{self.id}-{self.slug}"

    @property
    def points(self) -> int:
        return sum(c.points for c in self.challenges)
