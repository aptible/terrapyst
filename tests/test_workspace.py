import subprocess
from pathlib import Path
from unittest.mock import patch

from glom import glom

from terrapyst import TerraformWorkspace
from terrapyst.mixins import TerraformRun
from terrapyst.plan import TerraformPlan

from .conftest import PROVIDER_CACHE


def test_version():
    workspace = TerraformWorkspace()
    assert isinstance(workspace.version, str), "Version should be a string."


def test_init(workspace_environment):
    workspace = TerraformWorkspace(workspace_environment)
    workspace.env["TF_PLUGIN_CACHE_DIR"] = PROVIDER_CACHE
    workspace.init()
    assert (Path(workspace_environment) / ".terraform").is_dir(), "Workspace has initialized."


def test_init_with_custom_backend_conf(workspace_environment):
    with patch.object(subprocess, "run", wraps=subprocess.run) as wrapped_subprocess_call:
        workspace = TerraformWorkspace(
            workspace_environment, backend_config_path=Path(workspace_environment) / "mock.tfbackend"
        )
        workspace.env["TF_PLUGIN_CACHE_DIR"] = PROVIDER_CACHE
        workspace.init()
        assert any(["-backend-config=" in arg for arg in wrapped_subprocess_call.call_args.args[0]])
        assert (Path(workspace_environment) / ".terraform").is_dir(), "Workspace has initialized."


def test_plan(workspace):
    results, plan = workspace.plan(error_function=print, output_function=print)
    assert results.successful, "Terraform plan succeeded."
    assert glom(plan, "raw_plan.variables.test_string.value") == "yes, this is a test"
    assert isinstance(plan, TerraformPlan), "Terraform plan returned on successful plan."


def test_apply_interaction(workspace):
    results, apply_log = workspace.apply(error_function=print, output_function=print)
    assert results.returncode == 1, "Terraform apply failed when interaction is required."


def test_apply_auto_approve(workspace):
    results, apply_log = workspace.apply(auto_approve=True, error_function=print, output_function=print)
    assert results.returncode == 0, "Terraform apply succeeded."


def test_destroy_interaction(workspace):
    results, apply_log = workspace.destroy(error_function=print, output_function=print)
    assert results.returncode == 1, "Terraform apply failed when interaction is required."


def test_destroy_auto_approve(workspace):
    results, apply_log = workspace.destroy(auto_approve=True, error_function=print, output_function=print)
    assert results.returncode == 0, "Terraform apply succeeded."
