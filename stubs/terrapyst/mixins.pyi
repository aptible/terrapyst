from .exceptions import TerraformRuntimeError as TerraformRuntimeError
from _typeshed import Incomplete

logger: Incomplete
DEFAULT_ENV_VARS: Incomplete

class ProcessResults:
    returncode: Incomplete
    successful: Incomplete
    stdout: Incomplete
    stderr: Incomplete
    def __init__(self, returncode, stdout, stderr) -> None: ...

class TerraformRun: ...
