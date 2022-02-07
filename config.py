import os
# import secrets
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
# SECRET_KEY = secrets.token_hex()
load_dotenv()


class BaseConfig:
    """Base configuration."""

    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Ensure you set a secret key!')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    DATABASE = 'development.db'


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DATABASE = ':memory:'


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DATABASE = 'production.db'


config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
