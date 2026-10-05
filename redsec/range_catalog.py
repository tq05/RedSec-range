"""Schema and discovery for built-in and independently maintained ranges."""
from __future__ import annotations

from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

from .config import repo_root


class RangePort(BaseModel):
    name: str
    host: int = Field(ge=1, le=65535)
    container: int = Field(ge=1, le=65535)
    path: str = "/"


class RangeSource(BaseModel):
    repository: str
    revision: str
    branch: str = "main"

    @field_validator("revision")
    @classmethod
    def immutable_revision(cls, value: str) -> str:
        if len(value) != 40 or any(c not in "0123456789abcdef" for c in value.lower()):
            raise ValueError("revision must be a full 40-character Git commit")
        return value.lower()


class RangeRuntime(BaseModel):
    driver: Literal["builtin", "dockerfile", "adapter", "placeholder"]
    dockerfile: str | None = None
    command: list[str] = Field(default_factory=list)
    environment: dict[str, str] = Field(default_factory=dict)
    entrypoints: dict[str, list[str]] = Field(default_factory=dict)
    ports: list[RangePort] = Field(default_factory=list)
    health_port: str | None = None

    @model_validator(mode="after")
    def validate_runtime(self):
        if self.driver in {"dockerfile", "adapter"} and not self.dockerfile:
            raise ValueError(f"{self.driver} runtime requires dockerfile")
        names = [port.name for port in self.ports]
        if len(names) != len(set(names)):
            raise ValueError("port names must be unique within a range")
        if self.health_port and self.health_port not in names:
            raise ValueError("health_port must name a declared port")
        if any(not command for command in self.entrypoints.values()):
            raise ValueError("entrypoint commands cannot be empty")
        return self


class RangeChallenge(BaseModel):
    """A challenge implemented and maintained by an external range."""

    id: str
    title: str
    category: str
    difficulty: str
    variants: int = Field(default=1, ge=1)


class RangeCurriculum(BaseModel):
    """Discoverability and solution provenance for a cataloged range."""

    source: Literal["builtin", "upstream", "placeholder"]
    solution_status: Literal["redsec", "upstream", "unknown", "unavailable"]
    solution_url: str | None = None
    solution_path: str | None = None
    note: str | None = None
    challenges: list[RangeChallenge] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_curriculum(self):
        ids = [challenge.id for challenge in self.challenges]
        if len(ids) != len(set(ids)):
            raise ValueError("challenge IDs must be unique within a range")
        if self.solution_status == "upstream" and not self.solution_url:
            raise ValueError("upstream solutions require solution_url")
        return self


class RangeDefinition(BaseModel):
    id: str
    title: str
    maintainer: str
    homepage: str
    license: str
    availability: Literal["available", "placeholder"]
    aliases: list[str] = Field(default_factory=list)
    summary: str
    note: str | None = None
    source: RangeSource | None = None
    runtime: RangeRuntime
    curriculum: RangeCurriculum

    @model_validator(mode="after")
    def validate_source(self):
        external = self.runtime.driver in {"dockerfile", "adapter"}
        if external != (self.source is not None):
            raise ValueError("external runtimes require source; other runtimes must omit it")
        if self.availability == "placeholder" and self.runtime.driver != "placeholder":
            raise ValueError("placeholder ranges must use the placeholder driver")
        if external and not self.curriculum.challenges:
            raise ValueError("external ranges must enumerate their upstream challenges")
        if self.runtime.driver == "builtin" and self.curriculum.source != "builtin":
            raise ValueError("builtin runtime must use the builtin curriculum")
        if self.runtime.driver == "placeholder" and self.curriculum.source != "placeholder":
            raise ValueError("placeholder runtime must use the placeholder curriculum")
        return self


class RangeCatalog(BaseModel):
    version: int
    ranges: dict[str, RangeDefinition]

    @model_validator(mode="after")
    def validate_catalog(self):
        aliases: set[str] = set()
        host_ports: dict[int, str] = {}
        for range_id, definition in self.ranges.items():
            definition.id = range_id
            for alias in [range_id, *definition.aliases]:
                if alias in aliases:
                    raise ValueError(f"duplicate range id or alias: {alias}")
                aliases.add(alias)
            for port in definition.runtime.ports:
                if port.host in host_ports:
                    raise ValueError(
                        f"host port {port.host} shared by {range_id} and {host_ports[port.host]}"
                    )
                host_ports[port.host] = range_id
        return self

    def resolve(self, value: str) -> RangeDefinition:
        wanted = value.strip().lower()
        for definition in self.ranges.values():
            if wanted == definition.id or wanted in definition.aliases:
                return definition
        raise KeyError(value)


def catalog_path():
    return repo_root() / "ranges" / "catalog.yaml"


def load_catalog() -> RangeCatalog:
    raw = yaml.safe_load(catalog_path().read_text()) or {}
    ranges = raw.get("ranges", {})
    raw["ranges"] = {
        range_id: {"id": range_id, **(definition or {})}
        for range_id, definition in ranges.items()
    }
    return RangeCatalog.model_validate(raw)
