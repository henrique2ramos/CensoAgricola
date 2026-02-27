from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from helpers.logging import logger
from helpers.database import db
from models.Talhao import Talhao, TalhaoSchema


class TalhoesResources(Resource):
    def get(self):
        logger.info("GET request received for /talhoes endpoint")
        try:
            talhoes = Talhao.query.all()
            return TalhaoSchema(many=True).dump(talhoes), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar dados dos talhões."}, 500

    def post(self):
        logger.info("POST request received for /talhoes endpoint")
        try:
            data = request.get_json()
            talhao_data = TalhaoSchema().load(data)

            talhao = Talhao(
                propriedade_id=talhao_data['propriedade_id'],
                identificacao=talhao_data['identificacao'],
                area_cultivavel_ha=talhao_data['area_cultivavel_ha'],
                cultura=talhao_data['cultura'],
                tipo_solo=talhao_data.get('tipo_solo')
            )

            db.session.add(talhao)
            db.session.commit()

            return {"message": "Talhão criado com sucesso", "id": talhao.id}, 201
        except ValidationError as ve:
            return {"message": "Dados inválidos.", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar o talhão."}, 500


class TalhaoResources(Resource):
    def get(self, talhao_id):
        logger.info(f"GET request received for /talhoes/{talhao_id}")
        try:
            talhao = Talhao.query.filter_by(id=talhao_id).first()

            if not talhao:
                return {"message": "Talhão não encontrado."}, 404
            return TalhaoSchema().dump(talhao), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar dados do talhão."}, 500

    def put(self, talhao_id):
        logger.info(f"PUT request received for /talhoes/{talhao_id}")
        try:
            data = request.get_json()
            talhao_data = TalhaoSchema().load(data, partial=True)

            talhao = Talhao.query.filter_by(id=talhao_id).first()
            if not talhao:
                return {"message": "Talhão não encontrado."}, 404

            if 'identificacao' in talhao_data:
                talhao.identificacao = talhao_data.get('identificacao')
            if 'area_cultivavel_ha' in talhao_data:
                talhao.area_cultivavel_ha = talhao_data.get(
                    'area_cultivavel_ha')
            if 'cultura' in talhao_data:
                talhao.cultura = talhao_data.get('cultura')
            if 'tipo_solo' in talhao_data:
                talhao.tipo_solo = talhao_data.get('tipo_solo')

            db.session.commit()
            return {"message": "Talhão atualizado com sucesso", "id": talhao_id}, 200
        except ValidationError as ve:
            return {"message": "Dados inválidos.", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar talhão."}, 500

    def delete(self, talhao_id):
        logger.info(f"DELETE request received for /talhoes/{talhao_id}")
        try:
            talhao = Talhao.query.filter_by(id=talhao_id).first()
            if not talhao:
                return {"message": "Talhão não encontrado."}, 404

            db.session.delete(talhao)
            db.session.commit()
            return {"message": "Talhão deletado com sucesso", "id": talhao_id}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar talhão."}, 500
