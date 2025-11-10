from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

	app_name: str = Field(default="ERA")
	app_host: str = Field(default="127.0.0.1")
	app_port: int = Field(default=8000)

	database_url: str 
	redis_url: str 
	
	jwt_secret_key: str 
	jwt_algorithm: str = Field(default="HS256")



settings = Settings()