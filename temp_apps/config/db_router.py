import random


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        읽기 요청시에는 램덤으로 커넥션을 사용한다.
        """
        r = random.choice(["replica1", "replica2"])
        print(f"db_for_read {r}")

        return r

    def db_for_write(self, model, **hints):
        """
        쓰기 요청은 Primary데이터베이스 커넥션을 사용한다.
        """
        print("db_for_write")
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {"primary", "replica1", "replica2"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
