import logging
from dataclasses import MISSING, dataclass, fields
from typing import Optional

logger = logging.getLogger(__name__)


class MissingEnvironmentVariable(Exception):
    pass


def _read_env(field, env_vars):
    env_var = field.name.upper()
    if env_var in env_vars:
        return env_vars[env_var]
    elif field.default != MISSING:
        return field.default
    else:
        raise MissingEnvironmentVariable(
            f"Expected environment variable {env_var} was not set, exiting..."
        )


@dataclass
class SpineExporterConfig:
    splunk_url: str
    splunk_api_token_param_name: str
    output_spine_data_bucket: str
    s3_endpoint_url: Optional[str] = None

    @classmethod
    def from_environment_variables(cls, env_vars):
        return cls(**{field.name: _read_env(field, env_vars) for field in fields(cls)})
