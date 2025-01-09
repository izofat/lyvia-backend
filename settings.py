import os
from datetime import timedelta

import pydash
import toml

_script_dir = os.path.dirname(__file__)

config_path = os.path.join(_script_dir, "config.toml")

assert os.path.exists(
    config_path
), "config.toml not found. Use make config to create one."

config = toml.load(config_path)

assert config, "config.toml is empty, please fill it with the necessary data"

DEBUG = pydash.get(config, "debug", True)

IS_GLOBAL_API = pydash.get(config, "global_api", False)

ENV = "dev" if DEBUG else "prod"

API_PORT = pydash.get(config, f"api.{ENV}.port")

assert API_PORT, "API port not found in config.toml"

JWT_SECRET = pydash.get(config, "jwt_secret")

assert JWT_SECRET, "JWT secret not found in config.toml"

JWT_EXPIRATION_DELTA = timedelta(days=pydash.get(config, "jwt_expiration_delta", 5))

JWT_ALGORITHM = pydash.get(config, "jwt_algorithm", "HS256")

EMAIL_CODE_EXPIRATION_DELTA = timedelta(
    seconds=pydash.get(config, "email_code_expiration_delta", 300)
)


class MySqlConfig:
    HOST = pydash.get(config, f"db.{ENV}.host")
    PORT = pydash.get(config, f"db.{ENV}.port")
    USER = pydash.get(config, f"db.{ENV}.username")
    PASSWORD = pydash.get(config, f"db.{ENV}.password")
    DATABASE = pydash.get(config, f"db.{ENV}.database")
    POOL_SIZE = pydash.get(config, f"db.{ENV}.pool_size", 5)
    POOL_NAME = pydash.get(config, f"db.{ENV}.pool_name", "pool")


assert MySqlConfig.HOST, "Database host not found in config.toml"
assert MySqlConfig.PORT, "Database port not found in config.toml"
assert MySqlConfig.USER, "Database user not found in config.toml"
assert MySqlConfig.PASSWORD, "Database password not found in config.toml"
assert MySqlConfig.DATABASE, "Database name not found in config.toml"


class RedisConfig:
    HOST = pydash.get(config, f"redis.{ENV}.host")
    PORT = pydash.get(config, f"redis.{ENV}.port")

assert RedisConfig.HOST, "Redis host not found in config.toml"
assert RedisConfig.PORT, "Redis port not found in config.toml"
