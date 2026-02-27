from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from helpers.logging import logger
from helpers.database import db
from models.Propriedade import Propriedade, PropriedadeSchema


def _resolver_codigo_uf(propriedade_data):
    codigo_uf = propriedade_data.get('codigo_uf')
    codigo_ue = propriedade_data.get('codigo_ue')
    return codigo_uf if codigo_uf is not None else codigo_ue


class PropriedadesResources(Resource):
    def get(self):
        logger.info("GET request received for /propriedades endpoint")
        try:
            propriedades = Propriedade.query.all()
            return PropriedadeSchema(many=True).dump(propriedades), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar propriedades."}, 500

    def post(self):
        logger.info("POST request received for /propriedades endpoint")
        try:
            data = request.get_json()
            propriedade_data = PropriedadeSchema().load(data)
            codigo_uf = _resolver_codigo_uf(propriedade_data)

            propriedade = Propriedade(
                produtor_id=propriedade_data['produtor_id'],
                nome_propriedade=propriedade_data['nome_propriedade'],
                area_total_ha=propriedade_data['area_total_ha'],
                numero_car=propriedade_data.get('numero_car'),
                numero_ccir=propriedade_data.get('numero_ccir'),
                codigo_municipio=propriedade_data.get('codigo_municipio'),
                codigo_uf=codigo_uf,
                area_preservacao_ha=propriedade_data.get('area_preservacao_ha'),
                area_infraestrutura_ha=propriedade_data.get('area_infraestrutura_ha'),
                latitude=propriedade_data.get('latitude'),
                longitude=propriedade_data.get('longitude')
            )

            db.session.add(propriedade)
            db.session.commit()

            return {"message": "Propriedade criada com sucesso", "id": propriedade.id}, 201
        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar propriedade."}, 500


class PropriedadeResources(Resource):
    def get(self, propriedade_id):
        logger.info(f"GET request received for /propriedades/{propriedade_id}")
        try:
            propriedade = Propriedade.query.filter_by(id=propriedade_id).first()

            if not propriedade:
                return {"message": "Propriedade não encontrada"}, 404
            return PropriedadeSchema().dump(propriedade), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar propriedade."}, 500

    def put(self, propriedade_id):
        logger.info(f"PUT request received for /propriedades/{propriedade_id}")
        try:
            data = request.get_json()
            propriedade_data = PropriedadeSchema(partial=True).load(data)

            propriedade = Propriedade.query.filter_by(id=propriedade_id).first()
            if not propriedade:
                return {"message": "Propriedade não encontrada"}, 404

            if 'nome_propriedade' in propriedade_data:
                propriedade.nome_propriedade = propriedade_data.get('nome_propriedade')
            if 'numero_car' in propriedade_data:
                propriedade.numero_car = propriedade_data.get('numero_car')
            if 'numero_ccir' in propriedade_data:
                propriedade.numero_ccir = propriedade_data.get('numero_ccir')
            if 'codigo_municipio' in propriedade_data:
                propriedade.codigo_municipio = propriedade_data.get('codigo_municipio')
            if 'codigo_uf' in propriedade_data or 'codigo_ue' in propriedade_data:
                propriedade.codigo_uf = _resolver_codigo_uf(propriedade_data)
            if 'area_total_ha' in propriedade_data:
                propriedade.area_total_ha = propriedade_data.get('area_total_ha')
            if 'area_preservacao_ha' in propriedade_data:
                propriedade.area_preservacao_ha = propriedade_data.get('area_preservacao_ha')
            if 'area_infraestrutura_ha' in propriedade_data:
                propriedade.area_infraestrutura_ha = propriedade_data.get('area_infraestrutura_ha')
            if 'latitude' in propriedade_data:
                propriedade.latitude = propriedade_data.get('latitude')
            if 'longitude' in propriedade_data:
                propriedade.longitude = propriedade_data.get('longitude')

            db.session.commit()
            return {"message": "Propriedade atualizada com sucesso", "id": propriedade_id}, 200
        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar propriedade."}, 500

    def delete(self, propriedade_id):
        logger.info(
            f"DELETE request received for /propriedades/{propriedade_id}")
        try:
            propriedade = Propriedade.query.filter_by(id=propriedade_id).first()
            if not propriedade:
                return {"message": "Propriedade não encontrada"}, 404

            db.session.delete(propriedade)
            db.session.commit()
            return {"message": "Propriedade deletada com sucesso", "id": propriedade_id}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar propriedade."}, 500
