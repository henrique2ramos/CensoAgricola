from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Safra import Safra, SafraSchema


class SafraResources(Resource):
    def get(self):
        logger.info("GET request received for /safras endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = "SELECT * FROM safras"
            cursor.execute(statement)
            resultset = cursor.fetchall()
            safrasResponse = []
            for row in resultset:
                safra = Safra(
                    talhao_id=row[1],
                    nome_safra=row[2],
                    cultura=row[3],
                    variedade=row[4],
                    data_plantio_estimada=row[5],
                    data_colheita_estimada=row[6],
                    expectativa_producao=row[7]
                )
                safra.id = row[0]
                safrasResponse.append(SafraSchema().dump(safra))
            return safrasResponse, 200
        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "Erro ao buscar dados das safras."}, 500
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
                INSERT INTO safras (talhao_id, nome_safra, cultura, variedade, data_plantio_estimada, 
                                    data_colheita_estimada, expectativa_producao) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(statement, (
                str(safra_data['talhao_id']),
                safra_data['nome_safra'],
                safra_data['cultura'],
                safra_data.get('variedade'),
                safra_data.get('data_plantio_estimada'),
                safra_data.get('data_colheita_estimada'),
                safra_data.get('expectativa_producao')
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"id": str(new_id)}, 201
        except ValidationError as ve:
            logger.error(f"Validation error: {ve.messages}")
            return {"message": "Invalid input data.", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while creating the harvest record."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class SafraResource(Resource):
    def get(self, safra_id):
        logger.info(f"GET request received for /safras/{safra_id} endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = "SELECT * FROM safras WHERE id = %s"
            cursor.execute(statement, (str(safra_id),))
            row = cursor.fetchone()
            if row:
                safra = Safra(
                    talhao_id=row[1],
                    nome_safra=row[2],
                    cultura=row[3],
                    variedade=row[4],
                    data_plantio_estimada=row[5],
                    data_colheita_estimada=row[6],
                    expectativa_producao=row[7]
                )
                safra.id = row[0]
                return SafraSchema().dump(safra), 200
            else:
                return {"message": "Safra not found."}, 404
        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while fetching the harvest record."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
