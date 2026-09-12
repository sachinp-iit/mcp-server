import os
from typing import Any

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_DIR = os.path.join(BASE_DIR, "config", "prompts")

class PromptRegistry:
    """
    Enterprise-grade prompt registry
    - Multi-file loading
    - Domain separation
    - Lifecycle governance enforcement
    - Production gating
    - Safe defaults
    """

    def __init__(self, enforce_lifecycle: bool = True):
        self.enforce_lifecycle = enforce_lifecycle
        self.prompts: dict[str, Any] = {}
        self.meta: dict[str, Any] = {}
        self._load_all()

    def _load_all(self):
        if not os.path.exists(PROMPT_DIR):
            raise FileNotFoundError(f"Prompt directory not found: {PROMPT_DIR}")

        for file in sorted(os.listdir(PROMPT_DIR)):
            if not file.endswith(".yaml"):
                continue

            path = os.path.join(PROMPT_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            file_meta = data.get("meta", {})
            file_prompts = data.get("prompts", {})

            if not isinstance(file_prompts, dict):
               raise TypeError(f"Invalid prompt structure in {file}")

            # merge
            for name, prompt in file_prompts.items():
                if name in self.prompts:
                    raise RuntimeError(f"Duplicate prompt name detected: {name}")
                self.prompts[name] = prompt

            self.meta[file] = file_meta

    def get(self, name: str) -> dict[str, Any]:
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found in registry")

        prompt = self.prompts[name]

        if self.enforce_lifecycle:
            lifecycle = prompt.get("lifecycle", {})

            if lifecycle.get("state") != "active":
                raise RuntimeError(
                    f"[PROMPT BLOCKED] '{name}' state={lifecycle.get('state')}"
                )

            if lifecycle.get("approved") is not True:
                raise RuntimeError(
                    f"[PROMPT BLOCKED] '{name}' not approved"
                )

            if lifecycle.get("stage") != "production":
                raise RuntimeError(
                    f"[ENV BLOCKED] '{name}' stage={lifecycle.get('stage')}"
                )

        return prompt

    def list_prompts(self):
        return list(self.prompts.keys())

    def get_meta(self):
        return self.meta
