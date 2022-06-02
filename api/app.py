from flask import Flask, request
from flask_caching import Cache
from redis_config import Config
from controller.search_controller import SearchController
import logging


app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app)


# Decorator para verificar se irá limpar o cache
def verify_cache(f):
    def decorated(*args, **kwargs):
        cache_param = request.args.get('cache')
        if (cache_param is not None):
            if (cache_param.lower() == 'false'):
                cache.clear()
        return f(*args, **kwargs)
    return decorated


# Rota para consultar as musicas do artista
@app.route("/artist/<name>", methods=['GET'])
@verify_cache
@cache.cached(timeout=86400*7)
def get_artist(name):
    cache_param = request.args.get('cache')
    search = SearchController()

    # Verifica se veio o param cache, para consultar na API novamente
    # e salvar no DynamoDB.
    if (cache_param is not None):
        if (cache_param.lower() == 'false'):
            data = search.get_artist_api(name)
            uuid = search.save_data_artist(name, data['top_musics'])
            data['uuid'] = uuid
            return data

    # Se não veio o param cache, e não existe no cache
    # Verifica se existe no DynamoDB e retorna as informações
    exists_data = search.get_data_artist(name)
    if ('Item' in exists_data):
        logging.warning(exists_data)
        return {
            'status': True,
            'status_code': 200,
            'artist': exists_data['Item']['artist'],
            'top_musics': exists_data['Item']['data'],
            'uuid': exists_data['Item']['uuid']
        }

    # Caso não exista no DynamoDB, consulta e salva as informações
    data = search.get_artist_api(name)
    uuid = search.save_data_artist(name, data['top_musics'])
    data['uuid'] = uuid
    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
