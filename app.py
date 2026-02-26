from helpers.application import app, api
from helpers.database import db
from helpers.logging import logger

from resources.HomeResources import HomeResources
from resources.ProdutoresResources import ProdutoresResources, ProdutorResources
from resources.PropriedadesResources import PropriedadesResources, PropriedadeResources
from resources.TalhoesResources import TalhoesResources, TalhaoResources
from resources.SafrasResources import SafrasResources, SafraResources

api.add_resource(HomeResources, '/')
api.add_resource(ProdutoresResources, '/produtores')
api.add_resource(PropriedadesResources, '/propriedades')
api.add_resource(TalhoesResources, '/talhoes')
api.add_resource(SafrasResources, '/safras')


api.add_resource(ProdutorResources, '/produtores/<int:produtor_id>')
api.add_resource(PropriedadeResources, '/propriedades/<int:propriedade_id>')
api.add_resource(TalhaoResources, '/talhoes/<int:talhao_id>')
api.add_resource(SafraResources, '/safras/<int:safra_id>')

with app.app_context():
    db.create_all()
    logger.info("Banco de dados sincronizado com sucesso.")
