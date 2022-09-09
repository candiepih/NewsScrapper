"""
Module contains methods that handle loading env
variables from file .env
"""
import environ
import os

env = environ.Env()
env_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/.env'

env.read_env(env.str('ENV_PATH', env_path))
