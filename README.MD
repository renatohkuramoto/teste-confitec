# API Teste CONFITEC
O objeto do teste foi criar uma aplicação para consumir a API Genius e salvar o retorno no cache e no DynamoDB.


## Instalação

Subir a aplicação pelo docker-compose

```sh
docker-compose up
```

Após subir a aplicação no docker, ela estará disponível em http://127.0.0.1:5000

## Rotas

```sh
GET http://127.0.0.1:5000/artist/{name}
ou
GET http://127.0.0.1:5000/artist/{name}?cache=false
```


**Renato Kuramoto**
