# InTouch

[![python](https://img.shields.io/badge/python-3.12_-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.110.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.28-critical?style=flat-square)](https://www.sqlalchemy.org//)
[![alembic](https://img.shields.io/badge/alembic-1.13.1_-violet?style=flat-square)](https://alembic.sqlalchemy.org//)
[![rabbitmq](https://img.shields.io/badge/aiopika-red?style=flat-square)](https://aio-pika.readthedocs.io/en/latest/index.html)
[![kafka](https://img.shields.io/badge/aiokafka-black?style=flat-square)](https://aiokafka.readthedocs.io/en/stable/index.html)


## Techs-Patterns
- CQRS
- SAGA
- Microservices(links via aio-pika\aiokafka)


## Description

This is the super-app project with multiple features. For now, it's in development.

## Features
- Registration (creating user)
- Login\Logout\Refresh token\Check auth (custom features)
- Creating profile(creating user triggers creating profile with age, email, phone number, user id from intouch_auth)
- Add\Del friends