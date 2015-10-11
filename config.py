import os


basedir = os.path.abspath(os.path.dirname(__name__))

DATABASE = "flasktaskr.db"
CSRF_ENABLED = True
SECRET_KEY = "j\xa3\xf2 \xc8\x9fR*\x00\xbdh\xf0 \
    \x01\xd3O\xe5\xa1\xc5\x9f\n|\xf5\xce"

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
