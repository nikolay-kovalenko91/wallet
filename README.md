# Wallet

## How to run app locally
### 1) Install Docker and Docker Compose on your OS<br />
https://docs.docker.com/compose/install/

### 2) Apply DB migrations<br />
```$ docker-compose up -d db```<br />
```$ docker-compose run app python manage.py migrate```<br />

### 3) Run app<br />
```$ docker compose up app```<br />
The app address is http://0.0.0.0:8000/ <br />

## How to run code quality checks and tests<br />
You may need this before pushing to the repo
#### Lint: <br />
```$ flake8 .```<br />
#### Tests and coverage: <br />
```$ docker-compose run app pytest --cov=/usr/src/wallet /usr/src```<br />
