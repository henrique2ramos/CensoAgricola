from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Propriedade import Propriedade, PropriedadeSchema


class PropriedadesResources(Resource):
    def get(self):
        logger.info("GET request received for /propriedades endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, produtor_id, nome_propriedade, numero_car, numero_ccir, municipio, estado, area_total_ha, area_preservacao_ha, area_infraestrutura_ha, latitude, longitude FROM propriedades")
            resultset = cursor.fetchall()

            propriedades_response = []
            for row in resultset:
                propriedade = Propriedade(
                    produtor_id=row[1],
                    nome_propriedade=row[2],
                    numero_car=row[3],
                    numero_ccir=row[4],
                    municipio=row[5],
                    estado=row[6],
                    area_total_ha=row[7],
                    area_preservacao_ha=row[8],
                    area_infraestrutura_ha=row[9],
                    latitude=row[10],
                    longitude=row[11]
                )
                propriedade.id = row[0]
                propriedades_response.append(
                    PropriedadeSchema().dump(propriedade))

            return propriedades_response, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar propriedades."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self):
        logger.info("POST request received for /propriedades endpoint")
        conn = None
        try:
            data = request.get_json()
            propriedade_data = PropriedadeSchema().load(data)

            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                INSERT INTO propriedades (
                    produtor_id, nome_propriedade, numero_car, numero_ccir, 
                    municipio, estado, area_total_ha, area_preservacao_ha, 
                    area_infraestrutura_ha, latitude, longitude
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(statement, (
                propriedade_data['produtor_id'],
                propriedade_data['nome_propriedade'],
                propriedade_data.get('numero_car'),
                propriedade_data.get('numero_ccir'),
                propriedade_data.get('municipio'),
                propriedade_data.get('estado'),
                propriedade_data['area_total_ha'],
                propriedade_data.get('area_preservacao_ha'),
                propriedade_data.get('area_infraestrutura_ha'),
                propriedade_data.get('latitude'),
                propriedade_data.get('longitude')
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {"message": "Propriedade criada com sucesso", "id": new_id}, 201
        except ValidationError as ve:
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao criar propriedade."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class PropriedadeResources(Resource):
    def get(self, propriedade_id):
        logger.info(f"GET request received for /propriedades/{propriedade_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, produtor_id, nome_propriedade, numero_car, numero_ccir, municipio, estado, area_total_ha, area_preservacao_ha, area_infraestrutura_ha, latitude, longitude FROM propriedades WHERE id = %s", (propriedade_id,))
            row = cursor.fetchone()

            if not row:
                return {"message": "Propriedade não encontrada"}, 404

            propriedade = Propriedade(
                produtor_id=row[1], nome_propriedade=row[2], numero_car=row[3],
                numero_ccir=row[4], municipio=row[5], estado=row[6],
                area_total_ha=row[7], area_preservacao_ha=row[8],
                area_infraestrutura_ha=row[9], latitude=row[10], longitude=row[11]
            )
            propriedade.id = row[0]
            return PropriedadeSchema().dump(propriedade), 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao buscar propriedade."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def put(self, propriedade_id):
        logger.info(f"PUT request received for /propriedades/{propriedade_id}")
        conn = None
        try:
            data = request.get_json()
            propriedade_data = PropriedadeSchema().load(data, partial=True)
            conn = get_conn()
            cursor = conn.cursor()

            statement = """
                UPDATE propriedades SET 
                    nome_propriedade = %s, numero_car = %s, numero_ccir = %s, 
                    municipio = %s, estado = %s, area_total_ha = %s, 
                    area_preservacao_ha = %s, area_infraestrutura_ha = %s, 
                    latitude = %s, longitude = %s
                WHERE id = %s RETURNING id
            """
            cursor.execute(statement, (
                propriedade_data.get(
                    'nome_propriedade'), propriedade_data.get('numero_car'),
                propriedade_data.get(
                    'numero_ccir'), propriedade_data.get('municipio'),
                propriedade_data.get(
                    'estado'), propriedade_data.get('area_total_ha'),
                propriedade_data.get('area_preservacao_ha'), propriedade_data.get(
                    'area_infraestrutura_ha'),
                propriedade_data.get(
                    'latitude'), propriedade_data.get('longitude'),
                propriedade_id
            ))

            if not cursor.fetchone():
                return {"message": "Propriedade não encontrada"}, 404

            conn.commit()
            return {"message": "Propriedade atualizada com sucesso", "id": propriedade_id}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao atualizar propriedade."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete(self, propriedade_id):
        logger.info(
            f"DELETE request received for /propriedades/{propriedade_id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM propriedades WHERE id = %s RETURNING id", (propriedade_id,))
            if not cursor.fetchone():
                return {"message": "Propriedade não encontrada"}, 404
            conn.commit()
            return {"message": "Propriedade deletada com sucesso", "id": propriedade_id}, 200
        except Error as e:
            logger.error(f"Database error: {e}")
            return {"message": "Erro ao deletar propriedade."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
