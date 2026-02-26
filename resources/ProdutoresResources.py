from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Produtor import Produtor, ProdutorSchema


class ProdutoresResources(Resource):
    def get(self):
        logger.info("GET request received for /produtores endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nome_razao_social, documento, inscricao_estadual, tipo_vinculo, telefone, email, criado_em FROM produtores")
            resultset = cursor.fetchall()

            produtores_response = []
            for row in resultset:
                produtor = Produtor(
                    nome_razao_social=row[1],
                    documento=row[2],
                    inscricao_estadual=row[3],
                    tipo_vinculo=row[4],
                    telefone=row[5],
                    email=row[6]
                )
                produtor.id = row[0]
                produtor.criado_em = row[7]
                produtores_response.append(ProdutorSchema().dump(produtor))

            return produtores_response, 200

        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar produtores."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self):
        logger.info("POST request received for /produtores endpoint")
        conn = None
        try:
            data = request.get_json()
            produtor_data = ProdutorSchema().load(data)

            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                INSERT INTO produtores (nome_razao_social, documento, inscricao_estadual, tipo_vinculo, telefone, email)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(statement, (
                produtor_data['nome_razao_social'],
                produtor_data['documento'],
                produtor_data.get('inscricao_estadual'),
                produtor_data['tipo_vinculo'],
                produtor_data.get('telefone'),
                produtor_data.get('email')
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return {"message": "Produtor criado com sucesso", "id": new_id}, 201

        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar produtor."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class ProdutorResources(Resource):
    def get(self, produtor_id):
        logger.info(f"GET request received for /produtores/{produtor_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = "SELECT id, nome_razao_social, documento, inscricao_estadual, tipo_vinculo, telefone, email, criado_em FROM produtores WHERE id = %s"
            cursor.execute(statement, (produtor_id,))
            row = cursor.fetchone()

            if not row:
                return {"message": "Produtor não encontrado"}, 404

            produtor = Produtor(
                nome_razao_social=row[1],
                documento=row[2],
                inscricao_estadual=row[3],
                tipo_vinculo=row[4],
                telefone=row[5],
                email=row[6]
            )
            produtor.id = row[0]
            produtor.criado_em = row[7]

            return ProdutorSchema().dump(produtor), 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar produtor."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def put(self, produtor_id):
        logger.info(f"PUT request received for /produtores/{produtor_id}")
        conn = None
        try:
            data = request.get_json()
            produtor_data = ProdutorSchema().load(data, partial=True)

            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                UPDATE produtores 
                SET nome_razao_social = %s, 
                    documento = %s, 
                    inscricao_estadual = %s, 
                    tipo_vinculo = %s, 
                    telefone = %s, 
                    email = %s
                WHERE id = %s 
                RETURNING id
            """

            cursor.execute(statement, (
                produtor_data.get('nome_razao_social'),
                produtor_data.get('documento'),
                produtor_data.get('inscricao_estadual'),
                produtor_data.get('tipo_vinculo'),
                produtor_data.get('telefone'),
                produtor_data.get('email'),
                produtor_id
            ))

            updated_row = cursor.fetchone()

            if not updated_row:
                return {"message": "Produtor não encontrado"}, 404

            conn.commit()
            return {"message": "Produtor atualizado com sucesso", "id": updated_row[0]}, 200

        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar produtor."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete(self, produtor_id):
        logger.info(f"DELETE request received for /produtores/{produtor_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM produtores WHERE id = %s RETURNING id", (produtor_id,))
            deleted_row = cursor.fetchone()

            if not deleted_row:
                return {"message": "Produtor não encontrado"}, 404

            conn.commit()
            return {"message": "Produtor deletado com sucesso", "id": deleted_row[0]}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar produtor."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
