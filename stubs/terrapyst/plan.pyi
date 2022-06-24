from .exceptions import TerraformRuntimeError as TerraformRuntimeError, TerraformVersionError as TerraformVersionError
from .mixins import TerraformRun as TerraformRun
from _typeshed import Incomplete

logger: Incomplete
MODIFICATION_ACTIONS: Incomplete
DELETION_ACTIONS: Incomplete
CREATE_ACTIONS: Incomplete

class TerraformPlan(TerraformRun):
    cwd: Incomplete
    env: Incomplete
    raw_plan: Incomplete
    terraform_version: Incomplete
    format_version: Incomplete
    deletions: int
    creations: int
    modifications: int
    changes: Incomplete
    def __init__(self, cwd, plan_path) -> None: ...

class TerraformChange:
    address: Incomplete
    type: Incomplete
    actions: Incomplete
    def __init__(self, changeset) -> None: ...
    def will_delete(self): ...
    def will_modify(self): ...
    def will_create(self): ...
