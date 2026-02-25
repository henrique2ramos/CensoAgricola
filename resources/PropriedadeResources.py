from flask_restful import Resource
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Propriedade import Propriedade, PropriedadeSchema


class PropriedadeResources(Resource):
    def get(self):
        logger.info("GET request received for /propriedades endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            # SQL corrigido para bater com o banco de dados
            statement = """
                SELECT id, produtor_id, nome_propriedade, numero_car, numero_ccir, 
                       municipio, estado, area_total_ha, area_preservacao_ha, 
                       area_infraestrutura_ha, latitude, longitude 
                FROM propriedades
            """
            cursor.execute(statement)
            resultset = cursor.fetchall()

            propriedadesResponse = []
            for row in resultset:
                propriedade = Propriedade(
                    produtor_id=row[1],
                    nome_propriedade=row[2],
                    area_total_ha=row[7],
                    numero_car=row[3],
                    numero_ccir=row[4],
                    municipio=row[5],
                    estado=row[6],
                    area_preservacao_ha=row[8],  # Nome corrigido
                    area_infraestrutura_ha=row[9],
                    latitude=row[10],
                    longitude=row[11]
                )
                propriedade.id = row[0]
                propriedadesResponse.append(
                    PropriedadeSchema().dump(propriedade))

            return propriedadesResponse, 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "Erro ao buscar dados das propriedades."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

    def post(self):
        logger.info("POST request received for /propriedades endpoint")
        conn = None
        try:
            data = request.get_json()
            # Validação via Marshmallow (Schema)
            propriedade_data = PropriedadeSchema().load(data)

            conn = get_conn()
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO propriedades (
                    produtor_id, nome_propriedade, numero_car, numero_ccir, 
                    municipio, estado, area_total_ha, area_preservacao_ha, 
                    area_infraestrutura_ha, latitude, longitude
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            cursor.execute(insert_query, (
                propriedade_data['produtor_id'],
                propriedade_data['nome_propriedade'],
                propriedade_data.get('numero_car'),
                propriedade_data.get('numero_ccir'),
                propriedade_data['municipio'],
                propriedade_data['estado'],
                propriedade_data['area_total_ha'],
                propriedade_data.get('area_preservacao_ha'),  # Nome corrigido
                propriedade_data.get('area_infraestrutura_ha'),
                propriedade_data.get('latitude'),
                propriedade_data.get('longitude')
            ))
            new_id = cursor.fetchone()[0]
            conn.commit()

            return {"message": "Propriedade cadastrada com sucesso", "id": str(new_id)}, 201

        except ValidationError as ve:
            logger.error(f"Validation error: {ve.messages}")
            return {"message": "Dados inválidos", "errors": ve.messages}, 400
        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "Erro ao criar a propriedade."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()


class PropriedadeResource(Resource):
    def get(self, propriedade_id):
        logger.info(
            f"GET request received for /propriedades/{propriedade_id} endpoint")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statement = """
                SELECT id, produtor_id, nome_propriedade, numero_car, numero_ccir, 
                       municipio, estado, area_total_ha, area_preservacao_ha, 
                       area_infraestrutura_ha, latitude, longitude 
                FROM propriedades WHERE id = %s
            """
            cursor.execute(statement, (propriedade_id,))
            row = cursor.fetchone()

            if row is None:
                return {"message": "Propriedade não encontrada"}, 404

            propriedade = Propriedade(
                produtor_id=row[1],
                nome_propriedade=row[2],
                area_total_ha=row[7],
                numero_car=row[3],
                numero_ccir=row[4],
                municipio=row[5],
                estado=row[6],
                area_preservacao_ha=row[8],
                area_infraestrutura_ha=row[9],
                latitude=row[10],
                longitude=row[11]
            )
            propriedade.id = row[0]
            return PropriedadeSchema().dump(propriedade), 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "Erro ao buscar a propriedade."}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()
