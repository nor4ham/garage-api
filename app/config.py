from pydantic import BaseSettings
import os
from typing import List
from functools import lru_cache


class BaseConfig(BaseSettings):
    # db configs
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    # to disable docs if = None
    docs_url: str = "/docs"
    FORWARDED_ALLOW_IPS: str = "*"

    # the allowed browser sites requests
    default_allow_origins = ["*"]
    APP_NAME: str = "garage"
    ALLOWED_HOSTS: List[str] = ["*"]

    # timezone
    APP_TZ: str = "Asia/Riyadh"

    # this is for auto complate
    production: bool = False
    testing: bool = False

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def allow_hosts(self):
        if os.environ.get("ALLOWED_HOSTS") is None:
            return self.default_allow_origins
        else:
            return os.environ.get("ALLOWED_HOSTS").split(",")


class ProductionConfig(BaseConfig):
    production = True
    testing = False
    ENVIRONMENT = "prod"


class StagingConfig(BaseConfig):
    production = True
    testing = False
    ENVIRONMENT = "staging"


class TestingConfig(BaseConfig):
    production = False
    testing = True
    ENVIRONMENT = "testing"
    SQL_POOL_ENABLED = False


@lru_cache()
def current_config(ProductionConfig, StagingConfig, TestingConfig, BaseConfig):
    """
    this will load the required config passed on STAGE env if not set it will load LocalConfig
    """
    stage = os.environ.get("ENVIRONMENT", "local")

    if stage == "prod":
        config = ProductionConfig()
    elif stage == "staging":
        config = StagingConfig()
    elif stage == "testing":
        config = TestingConfig()
    elif stage == "local":
        config = BaseConfig()
    else:
        raise Exception(f"ENVIRONMENT: {stage} is not supported")

    return config


config: BaseConfig = current_config(
    ProductionConfig,
    StagingConfig,
    TestingConfig,
    BaseConfig,
)
