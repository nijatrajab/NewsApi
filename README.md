# PostAPI project

## Description

Welcome to PostAPI

## Getting Started

### Dependencies

* [Docker](https://www.docker.com/get-started)

### Installing

* Clone the repo
```
git clone https://github.com/nijatrajab/NewsApi.git
```
* Open `cmd` on cloned directory then follow commands:
```
docker-compose build
```

### Executing program

After creating docker images you can start containers for a service with 2 options
* On Docker Desktop start your containers using GUI or open `cmd` on cloned directory then follow commands:
```
docker-compose up
```
_Make sure Docker is running as an administrator. For the first time it may take a few minutes to start because of creating containers_

### Testing

After start your container open cmd on cloned directory then follow command:
```
docker-compose run news_app sh -c "python manage.py test && flake8"
```

## Postman

* Check out [Postman docs](https://go.postman.co/workspace/My-Workspace~8f1b1281-bc7b-42e4-80d9-c75507892478/collection/12709471-351fefec-dc17-4ac6-a28c-bc1a3193d96c)