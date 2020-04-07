import os
basedir = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/hospitalapp/static/img/photos'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/photos'
    UPLOADED_PHOTOS_DEST = TOP_LEVEL_DIR + '/hospitalapp/static/img/photos'
    UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/photos'
    
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'


