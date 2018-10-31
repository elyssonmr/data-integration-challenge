# Documentation


## Installation

This system just need to have [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed.

Then run the setup command in order to create the test container:
```shell
make setup
```

## Running

After installing all the docker requirements we could now run the tests and the API.

To run all unit tests:

```shell
make check
```

To start the API:

```shell
make start
```

The default port is **8000**.

## Endpoints Documentation

All API documentation is described in a [Swagger documentation](https://editor.swagger.io/?url=https://raw.githubusercontent.com/elyssonmr/data-integration-challenge/master/swagger.yml). There you can see all endpoints and examples about them.

Swagger also helps you create your client.
