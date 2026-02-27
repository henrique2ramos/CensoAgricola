from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from helpers.logging import logger
from helpers.database import db
from models.Safra import Safra, SafraSchema


class SafrasResources(Resource):
    def get(self):
        logger.info("GET request received for /safras endpoint")
        try:
            safras = Safra.query.all()
            return SafraSchema(many=True).dump(safras), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar safras."}, 500

    def post(self):
        logger.info("POST request received for /safras endpoint")
        try:
            data = request.get_json()
            safra_data = SafraSchema().load(data)

            safra = Safra(
                talhao_id=safra_data['talhao_id'],
                variedade=safra_data.get('variedade'),
                data_plantio_estimada=safra_data.get('data_plantio_estimada'),
                data_colheita_estimada=safra_data.get('data_colheita_estimada'),
                expectativa_producao=safra_data.get('expectativa_producao')
            )

            db.session.add(safra)
            db.session.commit()
            return {"message": "Safra criada com sucesso", "id": safra.id}, 201
        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar registro de safra."}, 500


class SafraResources(Resource):
    def get(self, safra_id):
        logger.info(f"GET request received for /safras/{safra_id}")
        try:
            safra = Safra.query.filter_by(id=safra_id).first()
            if safra:
                return SafraSchema().dump(safra), 200
            return {"message": "Safra não encontrada."}, 404
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar safra."}, 500

    def put(self, safra_id):
        logger.info(f"PUT request received for /safras/{safra_id}")
        try:
            data = request.get_json()
            safra_data = SafraSchema().load(data, partial=True)

            safra = Safra.query.filter_by(id=safra_id).first()
            if not safra:
                return {"message": "Safra não encontrada."}, 404

            if 'variedade' in safra_data:
                safra.variedade = safra_data.get('variedade')
            if 'data_plantio_estimada' in safra_data:
                safra.data_plantio_estimada = safra_data.get('data_plantio_estimada')
            if 'data_colheita_estimada' in safra_data:
                safra.data_colheita_estimada = safra_data.get('data_colheita_estimada')
            if 'expectativa_producao' in safra_data:
                safra.expectativa_producao = safra_data.get('expectativa_producao')

            db.session.commit()
            return {"message": "Safra atualizada com sucesso", "id": safra_id}, 200
        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar safra."}, 500

    def delete(self, safra_id):
        logger.info(f"DELETE request received for /safras/{safra_id}")
        try:
            safra = Safra.query.filter_by(id=safra_id).first()
            if not safra:
                return {"message": "Safra não encontrada."}, 404

            db.session.delete(safra)
            db.session.commit()
            return {"message": "Safra deletada com sucesso", "id": safra_id}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar safra."}, 500
