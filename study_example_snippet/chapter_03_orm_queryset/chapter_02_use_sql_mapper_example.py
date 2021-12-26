# ORM 없이 database에서 원하는 데이터를 조회하기
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Tuple

import psycopg2 as pg2


class UserSQLMapper:
    def get_user(self, pk) -> 'User':
        with pg2.connect(dbname='django_db', user='postgres', password='1234', host='127.0.0.1', port=5437) as conn:
            with conn.cursor() as cur:
                sql = """SELECT "user"."id", "user"."password", "user"."last_login", "user"."is_superuser",
                 "user"."username", "user"."first_name", "user"."last_name", "user"."email", "user"."is_staff",
                  "user"."is_active", "user"."date_joined", "user"."user_type", "user"."aa"
                  FROM "user" WHERE "user"."id" = %s"""
                cur.execute(sql, [pk])
                row = cur.fetchone()
                user = User(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    last_login=row[3],
                    is_superuser=row[4],
                    first_name=row[5],
                    last_name=row[6],
                    email=row[7],
                    is_staff=row[8],
                    is_active=row[9],
                    date_joined=row[10],
                )
        return user


@dataclass
class User:
    id: int
    username: str
    password: str
    last_login: datetime
    is_superuser: bool
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime

    sqlmapper = UserSQLMapper()


if __name__ == '__main__':

    # 데이터베이스에서 user의 id가 1인 데이터를 가져오는 함수를 만들었다! get_user()
    # 하지만 너무 시간이 많이 걸렸어 코드도 너무 지루해   // boilerplateCode가 발생함
    user: User = User.sqlmapper.get_user(pk=1)

    print('user: ', user)
