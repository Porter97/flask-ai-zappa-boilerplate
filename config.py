import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenSearch
    OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL')
    OPENSEARCH_USER = os.environ.get('OPENSEARCH_USER')
    OPENSEARCH_PASSWORD = os.environ.get('OPENSEARCH_PASSWORD')
    DOCUMENT_INDEX = os.environ.get('DOCUMENT_INDEX')
    CHAT_HISTORY_INDEX = os.environ.get('CHAT_HISTORY_INDEX')

    # Embeddings
    KNN_DIMENSIONS = os.environ.get('KNN_DIMENSIONS', 1536)

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

    # General
    SECRET_KEY = os.environ.get('SECRET_KEY')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    FLASK_CONFIG = 'DEV'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "data-dev.sqlite")}'
    TESTING = True
    DEBUG = True


class TestingConfig(Config):
    FLASK_CONFIG = 'TEST'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "data-test.sqlite")}'
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    FLASK_CONFIG = 'STAGING'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_POOL_SIZE = 1


class ProductionConfig(Config):
    FLASK_CONFIG = 'PROD'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_POOL_SIZE = 1


config = {
    'DEV': DevelopmentConfig,
    'TEST': TestingConfig,
    'STAGING': StagingConfig,
    'PROD': ProductionConfig,
}