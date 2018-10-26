#Challenge Makefile

start:
	docker-compose up -d --build

check:
	pytest --cov-report term-missing --cov=integration tests/

#setup:
#if needed to setup the enviroment before starting it
