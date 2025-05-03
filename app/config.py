"""Application configuration module using Pydantic Settings.

This module defines the `Settings` class for loading environment-specific
configuration values such as database connection details. Environment variables
are read from a `.env` file using `pydantic-settings`.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings model for environment configuration.

    Attributes:
        db_name (str): Name of the database.
        db_user (str): Username for the database connection.
        db_password (str): Password for the database connection.
        db_type (str): Type of the database (e.g., postgresql, mysql).
        db_host (str): Hostname or IP address of the database server.
        db_port (int): Port number on which the database is listening.

    Configuration:
        Loads values from a `.env` file and ignores any unknown fields.

    """

    db_name: str
    db_user: str
    db_password: str
    db_type: str
    db_host: str
    db_port: int

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()  # type: ignore
