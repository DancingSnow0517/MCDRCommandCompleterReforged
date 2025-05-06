from enum import StrEnum

# noinspection PyPackageRequirements
from mcdreforged.utils.serializer import Serializable


class CompletionMode(StrEnum):
    STDIO = "stdio"
    HTTP = "http"


class Config(Serializable):
    mode: CompletionMode = CompletionMode.HTTP
    http_port: int = 8080
