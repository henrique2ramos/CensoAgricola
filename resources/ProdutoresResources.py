from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from helpers.logging import logger
from helpers.database import db
from models.Produtor import Produtor, ProdutorSchema


def _normalizar_documento(valor):
    if valor is None:
        return None
    return ''.join(filter(str.isdigit, str(valor)))


def _resolver_documento_produtor(produtor_data, documento_atual=None):
    documento = produtor_data.get('documento')
    cpf = produtor_data.get('cpf')
    cnpj = produtor_data.get('cnpj')

    if cpf and cnpj:
        raise ValidationError({"cpf": ["Informe apenas CPF ou CNPJ."]})

    if cpf:
        documento = cpf
    if cnpj:
        documento = cnpj

    if documento is None:
        return documento_atual

    return _normalizar_documento(documento)


class ProdutoresResources(Resource):
    def get(self):
        logger.info("GET request received for /produtores endpoint")
        try:
            produtores = Produtor.query.all()
            return ProdutorSchema(many=True).dump(produtores), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar produtores."}, 500

    def post(self):
        logger.info("POST request received for /produtores endpoint")
        try:
            data = request.get_json()
            produtor_data = ProdutorSchema().load(data)
            documento = _resolver_documento_produtor(produtor_data)

            if not documento:
                return {"message": "Dados inválidos", "errors": {"documento": ["Informe CPF ou CNPJ."]}}, 400

            produtor = Produtor(
                nome_razao_social=produtor_data['nome_razao_social'],
                documento=documento,
                tipo_vinculo=produtor_data['tipo_vinculo'],
                inscricao_estadual=produtor_data.get('inscricao_estadual'),
                telefone=produtor_data.get('telefone'),
                email=produtor_data.get('email')
            )

            db.session.add(produtor)
            db.session.commit()

            return {"message": "Produtor criado com sucesso", "id": produtor.id}, 201

        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar produtor."}, 500


class ProdutorResources(Resource):
    def get(self, produtor_id):
        logger.info(f"GET request received for /produtores/{produtor_id}")
        try:
            produtor = Produtor.query.filter_by(id=produtor_id).first()

            if not produtor:
                return {"message": "Produtor não encontrado"}, 404

            return ProdutorSchema().dump(produtor), 200
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar produtor."}, 500

    def put(self, produtor_id):
        logger.info(f"PUT request received for /produtores/{produtor_id}")
        try:
            data = request.get_json()
            # Valida os dados, mas permite atualização parcial ou completa
            produtor_data = ProdutorSchema(partial=True).load(data)

            produtor = Produtor.query.filter_by(id=produtor_id).first()

            if not produtor:
                return {"message": "Produtor não encontrado"}, 404

            if 'nome_razao_social' in produtor_data:
                produtor.nome_razao_social = produtor_data.get(
                    'nome_razao_social')
            if 'documento' in produtor_data or 'cpf' in produtor_data or 'cnpj' in produtor_data:
                produtor.documento = _resolver_documento_produtor(
                    produtor_data, produtor.documento)
            if 'inscricao_estadual' in produtor_data:
                produtor.inscricao_estadual = produtor_data.get(
                    'inscricao_estadual')
            if 'tipo_vinculo' in produtor_data:
                produtor.tipo_vinculo = produtor_data.get('tipo_vinculo')
            if 'telefone' in produtor_data:
                produtor.telefone = produtor_data.get('telefone')
            if 'email' in produtor_data:
                produtor.email = produtor_data.get('email')

            db.session.commit()
            return {"message": "Produtor atualizado com sucesso", "id": produtor.id}, 200

        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar produtor."}, 500

    def delete(self, produtor_id):
        logger.info(f"DELETE request received for /produtores/{produtor_id}")
        try:
            produtor = Produtor.query.filter_by(id=produtor_id).first()

            if not produtor:
                return {"message": "Produtor não encontrado"}, 404

            deleted_id = produtor.id
            db.session.delete(produtor)
            db.session.commit()
            return {"message": "Produtor deletado com sucesso", "id": deleted_id}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar produtor."}, 500
