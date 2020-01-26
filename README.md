# Python scheduler app

This app inspects the data file here https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat and loops through each record, checking for duplicates before adding them to the database. 

Running locally via docker-compose
---

1. Run `docker-compose up -d`
2. Each time you want to try running the script, invoke `docker-compose up --build nfindocker`

Upon each invocation, the table will be recreated. You can change that by modifying `docker-compose.yml`'s
`command` section for `nfindocker` service - change `--initialize-table-recreate` to `--initialize-table`.

Inspect the table `data` at `localhost:25006`.


Running locally - external database
---

You need to have the following environment variables set:
- `DB_HOST` - database host
- `DB_PORT` - database port
- `DB_USER` - database user
- `DB_PASSWORD` - database password
- `DB_DATABASE` - database DB
- `DB_TABLE` - database table to use

The following options can be provided:
- `--initialize-table` - idempotent action, create table with correct schema as `DB_TABLE`
 if it does not exists, if it exists - do nothing
- `--initialize-table-recreate` - drops the table if it exists and then creates it again with correct schema
- `--url` - required, url of the source file to process.

Sample invocation
---
`DB_HOST=host DB_PORT=port DB_USER=user DB_PASSWORD=password DB_DATABASE=database DB_TABLE=table docker run nfindocker/pysamplerepo:latest --initialize-table --url=https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat`
