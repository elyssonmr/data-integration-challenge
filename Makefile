#Challenge Makefile

start:
#TODO: commands necessary to start the API

check:
	pytest --cov-report term-missing --cov=integration tests/

#setup:
#if needed to setup the enviroment before starting it
