import sqlite3

from helpers.application import app, api
from helpers.database import db, get_conn
from helpers.logging import logger

from resources.HomeResources import HomeResources
from resources.AgroResources import AgroResources

api.add_resource(HomeResources, '/')
api.add_resource(AgroResources, '/agro')


with app.app_context():
    db.create_all()
    db.create_all()
