import os

from dotenv import load_dotenv
from peewee import MySQLDatabase, Model

import threading


load_dotenv()


class SingletonInstance:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(SingletonInstance, cls).__new__(cls)
                cls._instance.__initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        with self._lock:
            if not getattr(self, '__initialized', False):
                self.__initialized = True
                self.initialize(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        pass  # Override this method in subclasses if needed


class DB(SingletonInstance):
    def initialize(self):
        self._db = MySQLDatabase(
            str(os.environ.get("MYSQL_DATABASE")),
            host="db",  # str(os.environ.get("MYSQL_HOST")),
            port=int(os.environ.get("MYSQL_PORT")),
            user=str(os.environ.get("MYSQL_USER")),
            password=str(os.environ.get("MYSQL_PASSWORD")),
            charset="utf8mb4",
        )

    @property
    def Base(self):
        return self._db

    def create_all(self, models: list[Model]):
        self.Base.create_tables(models)

    def connect(self):
        self.Base.connect()


class BaseModel(Model):
    class Meta:
        database = DB().Base
