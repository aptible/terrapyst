import json
import shutil
from logging import getLogger
from typing import Any, Dict

from .exceptions import TerraformRuntimeError, TerraformVersionError
from .mixins import TerraformRun

logger = getLogger(__name__)

MODIFICATION_ACTIONS = ["update"]
DELETION_ACTIONS = ["delete"]
CREATE_ACTIONS = ["create"]


class TerraformPlan(TerraformRun):
    changes: Dict[str, Any]
    env: Dict[str, str]

    def __init__(self, cwd, plan_path) -> None:
        # confirm file exists

        self.cwd = cwd
        self.env = {}
        self.plan_path = plan_path

        terraform_path = shutil.which("terraform")
        command = [terraform_path, "show", "-json", plan_path]
        results = self._subprocess_run(command)

        if results.returncode != 0:
            raise TerraformRuntimeError("Terraform plan failed", results)

        plan_details = json.loads(results.stdout)
        self.raw_plan = plan_details
        self.terraform_version = plan_details["terraform_version"]
        self.format_version = plan_details["format_version"]

        if self.format_version[:1] != "1":
            raise TerraformVersionError(
                f"Expected semantic version equivalent of v1, instead found '{self.format_version}'"
            )

        self.deletions = 0
        self.creations = 0
        self.modifications = 0

        self.changes = {}
        self._parse_changes(plan_details.get("resource_changes", []))

    def _parse_changes(self, change_plan: list):
        for changeset in change_plan:
            change = TerraformChange(changeset)
            self.changes[changeset["address"]] = TerraformChange(changeset)
            if change.will_delete():
                self.deletions += 1
            if change.will_create():
                self.creations += 1
            if change.will_modify():
                self.modifications += 1


class TerraformChange:
    def __init__(self, changeset) -> None:
        self.address = changeset["address"]
        self.type = changeset["type"]
        self.actions = changeset["change"]["actions"]

    def will_delete(self):
        return len(list(set(self.actions) & set(DELETION_ACTIONS))) > 0

    def will_modify(self):
        return len(list(set(self.actions) & set(MODIFICATION_ACTIONS))) > 0

    def will_create(self):
        return len(list(set(self.actions) & set(CREATE_ACTIONS))) > 0
