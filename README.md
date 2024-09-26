## Build and run the container

```shell
docker-compose up --build
```

## [Open swagger](http://localhost:8000/docs) to test the FastAPI app 
### !!! Don't use console output uvicorn link, because it redirects to docker container inner address, which is not available outside the container. Use the blue link above instead.

```
Database setup is stored in /postgre_sql/01_postgres_init.sql (executes automatically with docker container startup).
All dependencies, tables, triggers etc are presented there.
Database test population is stored in /postgre_sql/02_populate_database.sql (executes automatically with docker container startup).
```
```
Database pure-SQL tests are stored in /postgre_sql/test_database.sql.
FastAPI app provides a couple of endpoints with whole SQL functionality from the tech-task. 
```