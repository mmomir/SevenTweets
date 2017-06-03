import abc
import pg8000
from config import Config


class Migration(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def id(self):
        pass

    @abc.abstractclassmethod
    def upgrade(self, cursor):
        pass

    @abc.abstractclassmethod
    def downgrade(self, cursor):
        pass


class InitaialMigration(Migration):

    def id(self):
        return 1

    def upgrade(self, cursor):
        cursor.execute("CREATE TABLE tweets (id SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL, "
                       "tweet TEXT, created_at TIMESTAMP, type VARCHAR(20))")
        cursor.execute("CREATE TABLE network (id SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL, "
                       "server_address VARCHAR(30))")
    def downgrade(self, cursor):
        cursor.execute("DROP TABLE tweets")
        cursor.execute("DROP TABLE network")


class MigrationManager:

    UP = "up"
    DOWN = "down"

    def __init__(self, version_table="_migrations"):

        self.version_table = version_table
        self.db = pg8000.connect(**Config.DB_CONFIG)
        self.ensure_infrastructure()
        self.migrations = self.collect_migrations()

    def ensure_infrastructure(self):
        cur = self.db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS {} (version integer)".format(self.version_table))
        self.db.commit()
        cur.close()

    @staticmethod
    def collect_migrations():
        migrations = [cls() for cls in Migration.__subclasses__()]
        return sorted(migrations, key=lambda migration: migration.id())

    def migrate(self, direction):
        if direction not in [self.UP, self.DOWN]:
            raise ValueError("Invalid direction {}".format(direction))
        if direction == self.UP:
            self._upgrade()
        else:
            self._downgrade()

    def _upgrade(self):
        current_version = self.current_version()

        for migration in self.migrations:
            if migration.id() > current_version:
                cur = self.db.cursor()
                try:
                    migration.upgrade(cur)
                except:
                    self.db.rollback()
                    raise
                else:
                    self.set_version(migration.id())
                finally:
                    cur.close()

    def _downgrade(self):

        current_version = self.current_version()
        current_index = -1
        for i, migrations in enumerate(self.migrations):
            if migrations.id() == current_version:
                current_index = i

        cursor = self.db.cursor()
        try:
            self.migrations[current_index].downgrade(cursor)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        else:
            if current_index == 0:
                self.set_version(0)
            else:
                prev_migration = self.migrations[current_index - 1]
                self.set_version(prev_migration.id())
        finally:
            cursor.close()

    def current_version(self):
        cur = self.db.cursor()
        cur.execute("SELECT version FROM {} LIMIT 1".format(self.version_table))
        cur_version = cur.fetchone()
        if cur_version is None:
            version = 0
        else:
            version = cur_version[0]

        cur.close()
        return version

    def set_version(self, version):
        cur = self.db.cursor()
        cur.execute("SELECT count(*) FROM {}".format(self.version_table))
        count = cur.fetchone()[0]

        if count == 0:
            cur.execute("INSERT INTO {} (version) VALUES (%s)".format(self.version_table), (version,))
        else:
            cur.execute("UPDATE {} SET version=%s".format(self.version_table), (version,))
        self.db.commit()
        cur.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def __del__(self):
        try:
            self.db.close()

        except pg8000.core.InterfaceError:
            pass


def migrate(direction):
    with MigrationManager() as migrations:
        migrations.migrate(direction)