#Challenge Makefile

PWD = $(shell pwd)

start:
	docker-compose up -d --build

check:
	docker run --rm --name challange_test -v "${PWD}:/usr/app/" challange:latest pytest --cov-report term-missing --cov=/usr/app/integration /usr/app/tests/

setup:
	docker build -f Dockerfile-tests -t challange:latest .
