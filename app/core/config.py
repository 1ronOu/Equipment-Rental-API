from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AuthJWT(BaseSettings):
	private_key_path: Path = BASE_DIR / 'certs' / 'jwt_private.pem'
	public_key_path: Path = BASE_DIR / 'certs' / 'jwt_public.pem'
	algorithm: str = 'RS256'


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

	app_name: str = Field(default="ERA")
	app_host: str = Field(default="127.0.0.1")
	app_port: int = Field(default=8000)

	database_url: str
	redis_password: str
	redis_user: str
	redis_user_password: str
	redis_host: str
	redis_port: int

	jwt_secret_key: str
	jwt_algorithm: str = Field(default="HS256")

	auth_jwt: AuthJWT = AuthJWT()



settings = Settings()