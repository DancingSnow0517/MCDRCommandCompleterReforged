# noinspection PyPackageRequirements
from mcdreforged.utils.serializer import Serializable


class Config(Serializable):
    http_port: int = 8080
