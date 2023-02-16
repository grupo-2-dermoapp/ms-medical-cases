class Config(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///medical-cases.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False