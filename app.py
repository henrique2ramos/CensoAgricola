import sqlite3

from helpers.application import app, api
from helpers.database import db, get_conn
from helpers.logging import logger

from resources.HomeResources import HomeResources
from resources.ProdutorResources import ProdutorResource, ProdutorResources
from resources.PropriedadeResources import PropriedadeResources
from resources.TalhaoResources import TalhaoResources
from resources.SafraResources import SafraResources

api.add_resource(HomeResources, '/')
api.add_resource(ProdutorResources, '/produtores')
api.add_resource(ProdutorResource, '/produtores/<int:produtor_id>')
api.add_resource(PropriedadeResources, '/propriedades')
api.add_resource(TalhaoResources, '/talhoes')
api.add_resource(SafraResources, '/safras')

with app.app_context():
    db.create_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)