import sys
import os
import pytest

# Ensure project root on PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.prompt_loader import PromptRegistry

# Disable lifecycle enforcement for schema validation
registry = PromptRegistry(enforce_lifecycle=False)

EXPERIMENT_PROMPTS = {"ab_test_router", "prompt_evaluator"}

def test_registry_loads():
    prompts = registry.list_prompts()
    assert len(prompts) > 0

def test_lifecycle_state():
    for name in registry.list_prompts():
        p = registry.get(name)
        state = p["lifecycle"]["state"]

        # experiments are allowed to be testing
        if name in EXPERIMENT_PROMPTS:
            assert state in ["testing", "active"]
        else:
            assert state == "active"

def test_approval():
    for name in registry.list_prompts():
        p = registry.get(name)
        assert p["lifecycle"]["approved"] is True

def test_environment():
    for name in registry.list_prompts():
        p = registry.get(name)
        stage = p["lifecycle"]["stage"]

        # experiments are allowed in staging
        if name in EXPERIMENT_PROMPTS:
            assert stage in ["staging", "production"]
        else:
            assert stage == "production"

def test_compliance_schema():
    for name in registry.list_prompts():
        p = registry.get(name)
        c = p["compliance"]
        assert "pii" in c
        assert "gdpr" in c
        assert "logging_allowed" in c
        assert "training_allowed" in c
        assert "audit_required" in c

def test_observability_schema():
    for name in registry.list_prompts():
        p = registry.get(name)
        o = p["observability"]
        assert "tracing" in o
        assert "metrics" in o
        assert "logging" in o
        assert "sampling_rate" in o
        assert "trace_level" in o

def test_model_policy_schema():
    for name in registry.list_prompts():
        p = registry.get(name)
        m = p["model_policy"]
        assert "model" in m
        assert "temperature" in m
        assert "reasoning_effort" in m
        assert "deterministic" in m

def test_contract_schema():
    for name in registry.list_prompts():
        p = registry.get(name)
        c = p["contract"]
        assert "input" in c
        assert "output" in c
        assert "type" in c

def test_template_exists():
    for name in registry.list_prompts():
        p = registry.get(name)
        assert "template" in p
        assert isinstance(p["template"], str)
        assert len(p["template"].strip()) > 0
