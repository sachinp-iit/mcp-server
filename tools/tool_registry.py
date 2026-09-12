import os

import yaml


class ToolRegistryService:
    def __init__(self, registry: dict):
        self.registry = registry

    def resolve_by_intent(self, intent: str):
        for tool_name, meta in self.registry.items():
            if meta.get("operation") == intent:
                return tool_name
        raise ValueError(f"No tool registered for intent: {intent}")


def load_registry():
    path = os.getenv("TOOLS_YAML_PATH")
    with open(path) as f:
        return yaml.safe_load(f)["tools"]


def register(mcp):
    registry_data = load_registry()
    service = ToolRegistryService(registry_data)

    @mcp.tool()
    def resolve_tool_by_intent(intent: str) -> str:
        return service.resolve_by_intent(intent)
