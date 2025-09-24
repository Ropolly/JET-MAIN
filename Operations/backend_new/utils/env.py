from pydantic_settings import BaseSettings, SettingsConfigDict



# ASSIGNED VARIABLES DEFINE DEFUALTS (DEV)
# if there is not a value program will crash
# prod variables should already be loaded into environment before execution

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


    # BEGIN ENV VARIABLES
    # DEFAULTS ARE DEVELOPMENT VARIABLES
    DEBUG: bool = True
    SECRET_KEY: str = "DEV_KEYS_ARE_GREAT"
    ENCRYPTION_KEY: str
    ALLOWED_HOSTS: list[str]


    # TOKEN CREDENTIALS
    CSRF_TRUSTED_ORIGINS: list[str] = ['http://localhost','https://localhost']

    # DATABASE SETTINGS
    DB_NAME: str = "airmed"
    DB_USER: str = "airmed"
    DB_PASSWORD: str = "airmedpass"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    CORS_ALLOW_ALL_ORIGINS: bool = True

    # SMTP Email Settings
    EMAIL_HOST: str = "smtp.office365.com"
    EMAIL_PORT: str = "587"
    EMAIL_USER: str = "noreply@jeticu.com"
    EMAIL_PASS: str
    EMAIL_DEFAULT_FROM: str = "noreply@jeticu.com"

    ## EXTERNAL

    # flightaware
    AERO_API_KEY: str

    # docuseal
    DOCUSEAL_API_KEY: str
    DOCUSEAL_WEBHOOK_SECRET: str

    # authorize.net
    AUTH_NET_LOGIN_ID: str
    AUTH_NET_TRANS_ID: str

