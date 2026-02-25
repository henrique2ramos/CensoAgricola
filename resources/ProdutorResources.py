from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Produtor import Produtor, ProdutorSchema


class ProdutorResources(Resource):
    def get(self):
        logger.info("GET request received for /agro endpoint")
        try:
            conn = get_conn()
            cursor = conn.cursor()
            # Dica: Listar colunas explicitamente é mais seguro que SELECT *
            statement = "SELECT id, nome_razao_social, documento, inscricao_estadual, tipo_vinculo, telefone, email, criado_em FROM produtores"
            cursor.execute(statement)

            resultset = cursor.fetchall()

            produtoresResponse = []
            for row in resultset:
                # 1. Cria o objeto sem o ID no construtor
                produtor = Produtor(
                    nome_razao_social=row[1],
                    documento=row[2],
                    inscricao_estadual=row[3],
                    tipo_vinculo=row[4],
                    telefone=row[5],
                    email=row[6],
                    criado_em=row[7]
                )

                # 2. Atribui o ID manualmente para não dar erro de __init__
                produtor.id = row[0]

                produtoresResponse.append(ProdutorSchema().dump(produtor))

            return produtoresResponse, 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while fetching agricultural data."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self):
        logger.info("POST request received for /produtor endpoint")
        try:
            data = request.get_json()
            # O load do Marshmallow já valida os dados
            produtor_data = ProdutorSchema().load(data)

            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                INSERT INTO produtores (nome_razao_social, documento, inscricao_estadual, tipo_vinculo, telefone, email, criado_em)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(statement, (
                produtor_data['nome_razao_social'],
                produtor_data['documento'],
                produtor_data.get('inscricao_estadual'),
                produtor_data['tipo_vinculo'],
                produtor_data.get('telefone'),
                produtor_data.get('email'),
                produtor_data.get('criado_em')
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return {"message": "Produtor created successfully", "id": str(new_id)}, 201

        except ValidationError as ve:
            logger.error(f"Validation error: {ve.messages}")
            return {"message": "Invalid input data", "errors": ve.messages}, 400

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while creating the produtor."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class ProdutorResource(Resource):
    def get(self, produtor_id):
        logger.info(f"GET request received for /agro/{produtor_id} endpoint")
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = "SELECT id, nome_razao_social, documento, inscricao_estadual, tipo_vinculo, telefone, email, criado_em FROM produtores WHERE id = %s"
            cursor.execute(statement, (produtor_id,))

            row = cursor.fetchone()

            if row is None:
                return {"message": "Produtor not found"}, 404

            # Mesmo ajuste aqui: id fora do construtor
            produtor = Produtor(
                nome_razao_social=row[1],
                documento=row[2],
                inscricao_estadual=row[3],
                tipo_vinculo=row[4],
                telefone=row[5],
                email=row[6],
                criado_em=row[7]
            )
            produtor.id = row[0]

            return ProdutorSchema().dump(produtor), 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while fetching the produtor data."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete(self, produtor_id):
        logger.info(
            f"DELETE request received for /agro/{produtor_id} endpoint")
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = "DELETE FROM produtores WHERE id = %s RETURNING id"
            cursor.execute(statement, (produtor_id,))

            deleted_row = cursor.fetchone()

            if deleted_row is None:
                return {"message": "Produtor not found"}, 404

            conn.commit()
            return {"message": "Produtor deleted successfully", "id": str(deleted_row[0])}, 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while deleting the produtor."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    
    def put(self, produtor_id):
        logger.info(f"PUT request received for /produtor/{produtor_id} endpoint")
        try:
            data = request.get_json()
            # Valida os dados novos (partial=True permite atualizar apenas alguns campos)
            produtor_data = ProdutorSchema().load(data, partial=True)

            conn = get_conn()
            cursor = conn.cursor()

            # Gerar dinamicamente as colunas a serem atualizadas
            # Ou fixar as colunas principais:
            statement = """
                UPDATE produtores 
                SET nome_razao_social = %s, documento = %s, inscricao_estadual = %s, 
                    tipo_vinculo = %s, telefone = %s, email = %s
                WHERE id = %s RETURNING id
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
            if updated_row is None:
                return {"message": "Produtor not found"}, 404

            conn.commit()
            return {"message": "Produtor updated successfully", "id": str(updated_row[0])}, 200

        except ValidationError as ve:
            return {"message": "Invalid input data", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Error updating produtor"}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
