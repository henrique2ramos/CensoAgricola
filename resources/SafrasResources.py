from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Safra import Safra, SafraSchema


class SafrasResources(Resource):
    def get(self):
        logger.info("GET request received for /safras endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, talhao_id, cultura, variedade, data_plantio_estimada, data_colheita_estimada, expectativa_producao FROM safras")
            resultset = cursor.fetchall()

            safras_response = []
            for row in resultset:
                safra = Safra(
                    talhao_id=row[1],
                    cultura=row[2],
                    variedade=row[3],
                    data_plantio_estimada=row[4],
                    data_colheita_estimada=row[5],
                    expectativa_producao=row[6]
                )
                safra.id = row[0]
                safras_response.append(SafraSchema().dump(safra))
            return safras_response, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar safras."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self):
        logger.info("POST request received for /safras endpoint")
        conn = None
        try:
            data = request.get_json()
            safra_data = SafraSchema().load(data)

            conn = get_conn()
            cursor = conn.cursor()
            statement = """
                INSERT INTO safras (talhao_id, cultura, variedade, data_plantio_estimada, 
                                    data_colheita_estimada, expectativa_producao) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(statement, (
                safra_data['talhao_id'],
                safra_data['cultura'],
                safra_data.get('variedade'),
                safra_data.get('data_plantio_estimada'),
                safra_data.get('data_colheita_estimada'),
                safra_data.get('expectativa_producao')
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"message": "Safra criada com sucesso", "id": new_id}, 201
        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar registro de safra."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class SafraResources(Resource):
    def get(self, safra_id):
        logger.info(f"GET request received for /safras/{safra_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, talhao_id, cultura, variedade, data_plantio_estimada, data_colheita_estimada, expectativa_producao FROM safras WHERE id = %s", (safra_id,))
            row = cursor.fetchone()
            if row:
                safra = Safra(
                    talhao_id=row[1],
                    cultura=row[2],
                    variedade=row[3],
                    data_plantio_estimada=row[4],
                    data_colheita_estimada=row[5],
                    expectativa_producao=row[6]
                )
                safra.id = row[0]
                return SafraSchema().dump(safra), 200
            return {"message": "Safra não encontrada."}, 404
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar safra."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def put(self, safra_id):
        logger.info(f"PUT request received for /safras/{safra_id}")
        conn = None
        try:
            data = request.get_json()
            safra_data = SafraSchema().load(data, partial=True)
            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                UPDATE safras SET 
                    cultura = %s, variedade = %s, data_plantio_estimada = %s, 
                    data_colheita_estimada = %s, expectativa_producao = %s
                WHERE id = %s RETURNING id
            """
            cursor.execute(statement, (
                safra_data.get('cultura'),
                safra_data.get('variedade'),
                safra_data.get('data_plantio_estimada'),
                safra_data.get('data_colheita_estimada'),
                safra_data.get('expectativa_producao'),
                safra_id
            ))

            if not cursor.fetchone():
                return {"message": "Safra não encontrada."}, 404

            conn.commit()
            return {"message": "Safra atualizada com sucesso", "id": safra_id}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar safra."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete(self, safra_id):
        logger.info(f"DELETE request received for /safras/{safra_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM safras WHERE id = %s RETURNING id", (safra_id,))
            if not cursor.fetchone():
                return {"message": "Safra não encontrada."}, 404
            conn.commit()
            return {"message": "Safra deletada com sucesso", "id": safra_id}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar safra."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
