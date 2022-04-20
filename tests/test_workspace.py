from pathlib import Path

from glom import glom

from terrapy import TerraformWorkspace
from terrapy.plan import TerraformPlan

from .conftest import PROVIDER_CACHE


def test_version():
    workspace = TerraformWorkspace()
    assert isinstance(workspace.version, str), "Version should be a string."


def test_init(workspace_environment):
    workspace = TerraformWorkspace(workspace_environment)
    workspace.env["TF_PLUGIN_CACHE_DIR"] = PROVIDER_CACHE
    workspace.init()
    assert (Path(workspace_environment) / ".terraform").is_dir(), "Workspace has initialized."


def test_plan(workspace):
    results, plan = workspace.plan(error_function=print, output_function=print)
    assert results.successful, "Terraform plan succeeded."
    assert glom(plan, "raw_plan.variables.test_string.value") == "yes, this is a test"
    assert isinstance(plan, TerraformPlan), "Terraform plan returned on successfull plan."


def test_plan_with_custom_backend_conf(workspace_environment):
    workspace = TerraformWorkspace(workspace_environment)
    workspace.env["TF_PLUGIN_CACHE_DIR"] = PROVIDER_CACHE
    workspace.init(backend_config_path=Path(workspace_environment) / "mock.tfbackend")
    results, plan = workspace.plan(error_function=print, output_function=print)
    assert results.successful, "Terraform plan succeeded."
    assert glom(plan, "raw_plan.variables.test_string.value") == "yes, this is a test"
    assert isinstance(plan, TerraformPlan), "Terraform plan returned on successfull plan."


def test_apply_interaction(workspace):
    results = workspace.apply(error_function=print, output_function=print)
    assert results.returncode == 1, "Terraform apply failed when interaction is required."


def test_apply_auto_approve(workspace):
    results = workspace.apply(auto_approve=True, error_function=print, output_function=print)
    assert results.returncode == 0, "Terraform apply succeeded."
