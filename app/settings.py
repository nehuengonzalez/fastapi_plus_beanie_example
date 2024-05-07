from pydantic_settings import BaseSettings


class TaskServiceBaseSettings(BaseSettings):
    service_name: str = "task_service"
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = "tasked"
    mongo_password: str = "tasked"
    mongo_db_name: str = "celery_example_db"

    @property
    def mongo_url(self):
        mongo_url = 'mongodb://%s:%s@%s:%s/%s?authMechanism=SCRAM-SHA-1&authSource=admin' % (
            self.mongo_user,
            self.mongo_password,
            self.mongo_host,
            self.mongo_port,
            self.mongo_db_name
        )
        return mongo_url
