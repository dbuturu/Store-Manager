class Config(object):
    DEBUG = False


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