from config.config import get_redis


# Configurações de conexão do Redis
class Config(object):
    CACHE_TYPE = get_redis()['CACHE_TYPE']
    CACHE_REDIS_PORT = get_redis()['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = get_redis()['CACHE_REDIS_DB']
    CACHE_REDIS_URL = get_redis()['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = get_redis()['CACHE_DEFAULT_TIMEOUT']
