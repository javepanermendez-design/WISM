"""Runtime configuration for WIMS."""
import os


class Config:
    """Shared application settings."""
    SECRET_KEY = os.getenv("WIMS_SECRET_KEY", "wims-prototype-key")
    MYSQL_DATABASE_URL = os.getenv("WIMS_DATABASE_URL", "mysql+pymysql://user:password@localhost/wims")


class DevelopmentConfig(Config):
    """Development settings."""
    DEBUG = True


class ProductionConfig(Config):
    """Production settings."""
    DEBUG = False
