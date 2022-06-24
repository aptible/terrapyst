from _typeshed import Incomplete

class TerraformError(Exception): ...

class TerraformRuntimeError(TerraformError):
    process_results: Incomplete
    message: Incomplete
    def __init__(self, message, process_results) -> None: ...

class TerraformVersionError(TerraformError): ...
