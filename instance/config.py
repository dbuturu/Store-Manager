import os

class Config(object):
    DEBUG = False
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED=os.getenv("JWT_BLACKLIST_ENABLED")


class Development(Config):
    DEBUG = True
    ENV = 'development'


class Testing(Config):
    TESTING = True
    DEBUG = True
    ENV = 'testing'


class Production(Config):
    DEBUG = False
    TESTING = False
    ENV = 'production'


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}