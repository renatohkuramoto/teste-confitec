import requests
from uuid import uuid4
from config import get_url_services
from database import resource


class SearchController:
    def __init__(self):
        # Seta a URL e Token na classe
        self.__url_genius = get_url_services()['genius']
        self.__token_genius = get_url_services()['genius_auth']

    # Busca o Id do Artista
    def get_id_artist(self, artist):
        URL = self.__url_genius + '/search?q=' + artist
        headers = {'Authorization': f'Bearer {self.__token_genius}'}
        req = requests.get(URL, headers=headers)

        if (req.status_code == 200):
            id = req.json()['response']['hits'][0]['result']['primary_artist']['id']
            return {
                'status': True,
                'status_code': req.status_code,
                'id': id
            }
        return {
            'status': False,
            'status_code': req.status_code
        }

    # Busca as musicas do artista
    def get_artist_api(self, artist):
        data = self.get_id_artist(artist)
        if (data['status']):
            id = data['id']
            URL = self.__url_genius + f'/artists/{id}/songs?sort=popularity&per_page=10'
            headers = {'Authorization': f'Bearer {self.__token_genius}'}
            req = requests.get(URL, headers=headers)
            result = self.format_data(req.json())
            if (req.status_code == 200):
                return {
                    'status': True,
                    'status_code': req.status_code,
                    'artist': artist.upper(),
                    'top_musics': result
                }
            return {
                'status': False,
                'status_code': req.status_code
            }

    # Salva a consulta no DynamoDB
    def save_data_artist(self, artist, data):
        uuid = str(uuid4())
        artists_db = resource.Table('Artists')
        artists_db.put_item(
            Item={
                'uuid': uuid,
                'artist': artist.upper(),
                'data': data
            }
        )
        return uuid

    # Consulta os dados no DynamoDB
    def get_data_artist(self, artist):
        artists_db = resource.Table('Artists')
        response = artists_db.get_item(
            Key={'artist': artist},
            AttributesToGet=['artist', 'uuid', 'data']
            )

        return response

    # Armanzena as musicas em uma lista
    def format_data(self, data):
        list_songs = []
        for register in data['response']['songs']:
            list_songs.append(register['full_title'])
        return list_songs
