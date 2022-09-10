# NewsScrapper

`API` that serves data fetched from different websites. API is served through [`django web framework`](https://www.djangoproject.com/) that makes use of Redis for caching.

The web scraper powered by [`scrapy framework`](https://scrapy.org/) retrieves data from different urls and stores data to MongoDB. The web scraper runs under a `CRON` job that scrapes the data from the websites under a certain interval, and persists the data to a [`Mongo DB`](https://www.mongodb.com/) database for future retrieval.

Find [`live API by clicking here`](https://newscrapperapi.herokuapp.com/categories/technology)


# Get started

1. Git clone this repository on you machine.

```sh
git clone https://github.com/candiepih/NewsScrapper
```

2. After cloning navigate to the directory `NewsScrapper` and install all the dependencies from requirements.txt. 

  - `NB:` Before installing dependencies make sure you have activated the virtual environment

```sh
cd NewsScraper
pip install -r requirements.txt
```

3. After installing create a .env file with the following environment variables

```env
SECRET_KEY=<can be anything>
REDIS_URI=<YOUR REDIS URI>
REDIS_PASS=<REDIS PASSWORD IN ANY>
MONGODB_URI=<MONGO DB URI>
IS_DEVELOPMENT=<TRUE if environment is development otherwise FALSE>
```

when deploying make sure this env variables are configured.

4. You can now run the server with the following command

```sh
python manage.py runserver
```

5. Now you can open your browser under route `localhost:8000`
6. To run the spider open a new terminal and type the following command

```sh
scrapy crawl newsSpider
```
This will crawl the urls and persist data to mongo

# Routes

The API is served under the following routes

- `/` - Serves all the data from the api. After visiting this route you get the following response

![image](https://user-images.githubusercontent.com/44834632/189479654-f31ee188-4311-417d-a977-e310511d3ab5.png)

- `/categories` - Serves categories metadata. After visiting this route you get the following response

![image](https://user-images.githubusercontent.com/44834632/189479712-620efafa-2a00-495f-af47-e41a3c82feb9.png)

- `/categories/<category_name>`. Serves the category data. These are the available category names from `/categories` route. This will return the category with the following details

![image](https://user-images.githubusercontent.com/44834632/189479820-c075401a-c9e9-4987-88b2-fcd823255cff.png)

A single article has the following data:

![image](https://user-images.githubusercontent.com/44834632/189479879-e795eb0c-8977-4a5f-89e6-a1d34c74c70a.png)

# Folders

The following are the folders definations used in the project

- `api` - Contains configuration files for the api django app, i.e: views, urls
- `config` - Contains django project configurations
- `db` - Mongo db configuration
- `newsScraper` - Contains files related to the scrapy spider

