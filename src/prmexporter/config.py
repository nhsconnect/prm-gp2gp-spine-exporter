import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class MissingEnvironmentVariable(Exception):
    pass


class EnvConfig:
    def __init__(self, env_vars):
        self._env_vars = env_vars

    def read_env(self, name) -> str:
        try:
            return self._env_vars[name]
        except KeyError:
            raise MissingEnvironmentVariable(
                f"Expected environment variable {name} was not set, exiting..."
            )


@dataclass
class SpineExporterConfig:
    splunk_url: str
    splunk_api_token: str

    @classmethod
    def from_environment_variables(cls, env_vars):
        env = EnvConfig(env_vars)
        return SpineExporterConfig(
            splunk_url=env.read_env("SPLUNK_URL"), splunk_api_token=env.read_env("SPLUNK_API_TOKEN")
        )
