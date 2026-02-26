from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Talhao import Talhao, TalhaoSchema


class TalhoesResources(Resource):
    def get(self):
        logger.info("GET request received for /talhoes endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, propriedade_id, identificacao, area_cultivavel_ha, tipo_solo FROM talhoes")
            resultset = cursor.fetchall()

            talhoes_response = []
            for row in resultset:
                talhao = Talhao(
                    propriedade_id=row[1],
                    identificacao=row[2],
                    area_cultivavel_ha=row[3],
                    tipo_solo=row[4]
                )
                talhao.id = row[0]
                talhoes_response.append(TalhaoSchema().dump(talhao))

            return talhoes_response, 200
        except Error as e:
            logger.error(f"Database error: {e}")
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
                talhao_data['propriedade_id'],  # Agora é Integer
                talhao_data['identificacao'],
                talhao_data['area_cultivavel_ha'],
                talhao_data.get('tipo_solo')
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {"message": "Talhão criado com sucesso", "id": new_id}, 201
        except ValidationError as ve:
            return {"message": "Dados inválidos.", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar o talhão."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class TalhaoResources(Resource):
    def get(self, talhao_id):
        logger.info(f"GET request received for /talhoes/{talhao_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, propriedade_id, identificacao, area_cultivavel_ha, tipo_solo FROM talhoes WHERE id = %s", (talhao_id,))
            row = cursor.fetchone()

            if not row:
                return {"message": "Talhão não encontrado."}, 404

            talhao = Talhao(
                propriedade_id=row[1],
                identificacao=row[2],
                area_cultivavel_ha=row[3],
                tipo_solo=row[4]
            )
            talhao.id = row[0]
            return TalhaoSchema().dump(talhao), 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar dados do talhão."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def put(self, talhao_id):
        logger.info(f"PUT request received for /talhoes/{talhao_id}")
        conn = None
        try:
            data = request.get_json()
            talhao_data = TalhaoSchema().load(data, partial=True)
            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                UPDATE talhoes SET 
                    identificacao = %s, area_cultivavel_ha = %s, tipo_solo = %s
                WHERE id = %s RETURNING id
            """
            cursor.execute(statement, (
                talhao_data.get('identificacao'),
                talhao_data.get('area_cultivavel_ha'),
                talhao_data.get('tipo_solo'),
                talhao_id
            ))

            if not cursor.fetchone():
                return {"message": "Talhão não encontrado."}, 404

            conn.commit()
            return {"message": "Talhão atualizado com sucesso", "id": talhao_id}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar talhão."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete(self, talhao_id):
        logger.info(f"DELETE request received for /talhoes/{talhao_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM talhoes WHERE id = %s RETURNING id", (talhao_id,))
            if not cursor.fetchone():
                return {"message": "Talhão não encontrado."}, 404
            conn.commit()
            return {"message": "Talhão deletado com sucesso", "id": talhao_id}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar talhão."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
