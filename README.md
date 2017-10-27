# Flask Rest Interface

## General
This is a very basic PoC for a REST API build with Flask. 

## Setup
Data will by default be stored in `app.db` using sqlite. If you want to use a more reliable database, set `DATABASE_URL` as your environment variable wth a string like the following:
```
DATABASE_URL='mysql+pymysql://<user>:<password>@<host>:<port>/<db>'
```
For a Postgres DB use
```
DATABASE_URL='postgresql+psycopg2://<user>:<password>@<host>:<port>/<db>'
```

## Usage
By default, the application will listen on Port `5000`. Ideally, host a reverse proxy to redirect traffic or use the Docker Port Mapping feature.

A short healthcheck can be done by accessing the root URL. To fill the DB, use the `/collect` endpoint. It will automatically add 600 Items from the Zalando API to the DB. After that, the `/all` endpoint will return all entries at once - this is only meant to be used by the appropiate tools, since it may crash a browser.

Further querying can be done with the `/search` endpoint, which can be used with the following parameters:

| Parameter name | Description   |
| -------------  | ------------- |
| q              | A text query which will be used. Unless c is specified, it will search the Brand and the Name |
| c              | Restricts searching to a certain column, product_name or brand                                |
| per_page       | How many items should be shown per page. Defaults to 10                                       |
| page           | which Page is shown. Defaults to 1                                                            |
| sort           | Which column should be used to sort the results. Defaults to price, also allowed are product_name and brand |
| direction      | The Sorting direction. Can be asc or desc, defaults to asc                                    |


Basic Unit tests are provided within the `tests.py` file.

## Docker
Use `docker build . -t flaskrest` to build an docker image. Remember to set the env variable, otherwise the data will be lost when you delete the container. Please also keep in mind that atm. the unit tests are not added to the Docker Image - but feel free to include them.
