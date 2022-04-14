import json
import shutil
import subprocess

from .mixins import TerraformRun

MODIFICATION_ACTIONS = ["update"]
DELETION_ACTIONS = ["delete"]
CREATE_ACTIONS = ["create"]


class TerraformPlan(TerraformRun):
    def __init__(self, cwd, plan_path) -> None:
        # confirm file exists

        self.cwd = cwd
        self.env = {}

        terraform_path = shutil.which("terraform")
        command = [terraform_path, "show", "-json", plan_path]
        results = self._subprocess_run(command)

        if results.returncode != 0:
            print(results.stdout)
            print(results.stderr)
            raise Exception()

        plan_details = json.loads(results.stdout)
        self.raw_plan = plan_details
        self.terraform_version = plan_details["terraform_version"]
        self.format_version = plan_details["format_version"]

        if self.format_version[:1] != "1":
            raise Exception()

        self.deletions = 0
        self.creations = 0
        self.modifications = 0

        self.changes = {}
        for changeset in plan_details["resource_changes"]:
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
