from django.db.backends.postgresql.client import DatabaseClient as PostgresqlDatabaseClient


class DatabaseClient(PostgresqlDatabaseClient):
    ...