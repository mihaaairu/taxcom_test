## Build and run the container

```shell
docker-compose up --build
```

## [Open swagger](http://localhost:8000/docs) to test the FastAPI app 
### !!! Don't use console output uvicorn link, because it redirects to docker container inner address, which is not available outside the container. Use the blue link above instead.


> Database setup is stored in [01_postgres_init.sql](postgre_sql%2F01_postgres_init.sql) (executes automatically with docker container startup).  
All dependencies, tables, triggers etc. are presented there.  
Database test population is stored in [02_populate_database.sql](postgre_sql%2F02_populate_database.sql) (executes automatically with docker container startup).  

>Database pure-SQL tests are stored in [test_database.sql](postgre_sql%2Ftest_database.sql).  
FastAPI app provides a couple of endpoints with whole SQL functionality from the tech-task.   
