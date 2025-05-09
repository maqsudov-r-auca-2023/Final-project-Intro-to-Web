import os

SECRET_KEY = 'dev'
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'instance', 'mindspace.sqlite')
