from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Talhao import Talhao, TalhaoSchema

class TalhaoResources(Resource):
    def get(self):
        logger.info("GET request received for /talhoes endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = "SELECT id, propriedade_id, identificacao, area_cultivavel_ha, tipo_solo FROM talhoes"
            cursor.execute(statement)
            resultset = cursor.fetchall()

            talhoesResponse = []
            for row in resultset:
                talhao = Talhao(
                    propriedade_id=row[1],
                    identificacao=row[2],
                    area_cultivavel_ha=row[3],
                    tipo_solo=row[4]
                )
                talhao.id = row[0]
                talhoesResponse.append(TalhaoSchema().dump(talhao))

            return talhoesResponse, 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "Erro ao buscar dados dos talhões."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self):
        logger.info("POST request received for /talhoes endpoint")
        conn = None
        try:
            data = request.get_json()
            talhao_data = TalhaoSchema().load(data)

            conn = get_conn()
            cursor = conn.cursor()
            statement = """
                INSERT INTO talhoes (propriedade_id, identificacao, area_cultivavel_ha, tipo_solo) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """
            cursor.execute(statement, (
                str(talhao_data['propriedade_id']),
                talhao_data['identificacao'],
                talhao_data['area_cultivavel_ha'],
                talhao_data.get('tipo_solo')
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {"id": str(new_id)}, 201

        except ValidationError as ve:
            logger.warning(f"Validation error: {ve.messages}")
            return {"message": "Dados inválidos.", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "Erro ao criar o talhão."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()