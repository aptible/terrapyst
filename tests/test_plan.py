from pathlib import Path

import pytest

PLAN_FILE = Path(__file__).parent.absolute() / "terraform" / "plans" / "test.plan"


@pytest.fixture
def plan(workspace):
    results, plan = workspace.plan()
    return plan


def test_load(plan):
    assert plan.format_version == "1.0"
    assert plan.deletions == 0, "Nothing to delete."
    assert plan.deletions == 0, "Nothing to modify."
    assert plan.creations == 7, "Creating 7 resources."
