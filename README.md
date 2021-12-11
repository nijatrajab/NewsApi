# PostAPI project

## Description

Welcome to NewsAPI

## NewsAPI live on Heroku

* Visit [NewsAPIProject Swagger](https://news-api-post.herokuapp.com/swagger/) version
    
    On live version you need authenticate for using API endpoints. Follow steps for authentication:
    1. Go to user APIs and click `register` ![user apis](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20apis.png?raw=true)
    2. Then click `Try it out` ![user register](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20register.png?raw=true)
    3. Enter valid information, then click `execute` ![user register execute](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20register%20execute.png?raw=true)
    4. After `execute` you should see `Code 201` if your register information is valid ![user register 201](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20register%20201.png?raw=true)
    5. Then go back to the user APIs and click on `token` to get the token ![user token]![user apis](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20apis.png?raw=true)
    6. Click `Try it out` ![user token](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20token.png?raw=true)
    7. Enter valid information, then click `execute` ![user token execute](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20token%20execute.png?raw=true)
    8. After `execute` you should see `Code 200` if your have entered valid credentials. Then copy the `token` in the response body ![user token 200](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/user%20token%20200.png?raw=true)
    9. Go to top and click `Authorize` ![authorize](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/authorize.png?raw=true)
    10. Enter the copied token as shown in the example => `Token ************`. Then click `Authorize` ![user authorize](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/authorize%20execute.png?raw=true)
    
    After completing these steps, you can use the News API endpoints.
    
    For log out click `Authorize`, then click `Logout`![user logout](https://github.com/nijatrajab/NewsApi/blob/main/README_pic/auth%20logout.png?raw=true)


* Visit [NewsAPIProject Redoc](https://news-api-post.herokuapp.com/redoc/) version

## Setup for local development

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

* Check out [Postman docs](https://www.postman.com/nijatrajab/workspace/newsapi/collection/12709471-351fefec-dc17-4ac6-a28c-bc1a3193d96c)
