VERSION = "0.0.1"
from . import _version
from .apply_log import TerraformApplyLog
from .authentication import TerraformAuthentication
from .exceptions import TerraformError, TerraformRuntimeError, TerraformVersionError
from .plan import TerraformChange, TerraformPlan
from .workspace import TerraformWorkspace

__version__ = _version.get_versions()["version"]
