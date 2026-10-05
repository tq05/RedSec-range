import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / ".devcontainer" / "devcontainer.json"


def _config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def test_codespaces_devcontainer_has_runtime_and_lifecycle():
    config = _config()

    assert config["build"] == {"dockerfile": "Dockerfile"}
    assert any("docker-in-docker:4" in key for key in config["features"])
    assert any("node:1" in key for key in config["features"])
    assert any("sshd:1" in key for key in config["features"])
    assert config["postCreateCommand"] == "./scripts/codespaces-setup.sh"
    assert config["postStartCommand"] == "./scripts/codespaces-up.sh"
    assert config["hostRequirements"] == {
        "cpus": 4,
        "memory": "8gb",
        "storage": "32gb",
    }


def test_codespaces_ports_are_declared_private_by_default():
    config = _config()
    expected = {9010, 9020, 9030, 9040, 9050, 9060, 9070, 9071,
                9080, 9090, 9091, 9110, 9112}

    assert set(config["forwardPorts"]) == expected
    assert set(map(int, config["portsAttributes"])) == expected
    assert all(
        attributes["onAutoForward"] == "silent"
        and "visibility" not in attributes
        for attributes in config["portsAttributes"].values()
    )
    assert config["otherPortsAttributes"] == {"onAutoForward": "ignore"}


def test_codespaces_scripts_are_executable_and_valid_bash():
    scripts = [
        ROOT / "scripts" / "codespaces-setup.sh",
        ROOT / "scripts" / "codespaces-up.sh",
        ROOT / "scripts" / "codespaces-connect.sh",
    ]

    for script in scripts:
        assert os.access(script, os.X_OK)
        subprocess.run(["bash", "-n", script], check=True)


def test_codespaces_is_the_documented_default_cloud_path():
    readme = (ROOT / "README.md").read_text()
    agent_instructions = (ROOT / "AGENTS.md").read_text()

    assert "https://codespaces.new/tq05/RedSec-range?quickstart=1" in readme
    assert "docs/codespaces.md" in readme
    assert "Default GitHub Codespaces workflow" in agent_instructions
