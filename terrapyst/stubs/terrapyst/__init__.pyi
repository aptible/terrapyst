from .authentication import TerraformAuthentication as TerraformAuthentication
from .exceptions import TerraformError as TerraformError, TerraformRuntimeError as TerraformRuntimeError, TerraformVersionError as TerraformVersionError
from .plan import TerraformChange as TerraformChange, TerraformPlan as TerraformPlan
from .workspace import TerraformWorkspace as TerraformWorkspace

VERSION: str
