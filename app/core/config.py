from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AuthJWT(BaseSettings):
	private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
	public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
	algorithm: str = 'RS256'
	access_token_expire_minutes: int = 15
	refresh_token_expire_days: int = 30

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

	app_name: str = Field(default="ERA")
	app_host: str = Field(default="127.0.0.1")
	app_port: int = Field(default=8000)

	database_url: str = Field(default="postgresql+asyncpg://user:password@host:5432/db_name")
	redis_password: str = Field(default="<PASSWORD>")
	redis_user: str = Field(default="user")
	redis_user_password: str = Field(default="<PASSWORD>")
	redis_host: str = Field(default="127.0.0.1")
	redis_port: int = Field(default=6379)

	jwt_secret_key: str = Field(default="secret")
	jwt_algorithm: str = Field(default="HS256")

	auth_jwt: AuthJWT = AuthJWT()



settings = Settings()