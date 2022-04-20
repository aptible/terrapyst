import shutil
import tempfile
from pathlib import Path

import pytest

from terrapy import TerraformWorkspace

WORKSPACE_TEMPLATE = Path(__file__).parent.absolute() / "terraform" / "workspace"

# Speed up `init` functions by caching providers locally.
# This will be deleted between runs.
PROVIDER_CACHE = tempfile.mkdtemp()


@pytest.fixture
def workspace_environment(tmpdir):
    shutil.copytree(WORKSPACE_TEMPLATE, tmpdir, dirs_exist_ok=True)
    return tmpdir


@pytest.fixture
def workspace(workspace_environment):
    workspace = TerraformWorkspace(workspace_environment)
    workspace.env["TF_PLUGIN_CACHE_DIR"] = PROVIDER_CACHE
    workspace.init()
    return workspace


@pytest.fixture
def plan(workspace):
    results, plan = workspace.plan()
    return plan
