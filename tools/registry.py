import os
import yaml

def load_registry():
    path = os.getenv("TOOLS_YAML_PATH")
    if not path:
        raise RuntimeError("TOOLS_YAML_PATH is not set")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return data["tools"]

def register(mcp):
    registry_data = load_registry()

    @mcp.tool()
    def resolve_tool_by_intent(intent: str) -> str:
        for tool_name, meta in registry_data.items():
            if meta.get("operation") == intent:
                return tool_name
        raise ValueError(f"No tool registered for intent: {intent}")

_registry_cache = None

def _get_registry():
    global _registry_cache
    if _registry_cache is None:
        _registry_cache = load_registry()
    return _registry_cache

def resolve_tool_by_intent(intent: str) -> str:
    registry_data = _get_registry()
    for tool_name, meta in registry_data.items():
        if meta.get("operation") == intent:
            return tool_name
    raise ValueError(f"No tool for intent: {intent}")