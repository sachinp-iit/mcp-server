from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

# Reuse the existing project prompt directory
PROMPT_DIR = Path(__file__).resolve().parents[2] / "config" / "prompts"

_environment = Environment(
    loader=FileSystemLoader(PROMPT_DIR),
    undefined=StrictUndefined,
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

def renderer_prompt(template_name: str, **varaibles: object) -> str:
    """Render a Jinja2 prompt template with strict variable checking."""
    
    template = _environment.get_template(template_name)
    return template.render(**varaibles)