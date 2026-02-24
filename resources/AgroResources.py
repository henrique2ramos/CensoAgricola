from flask_restful import Resource
from models.Agricola import Agricola
from flask import request
from psycopg2 import Error
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Agricola import Agricola, AgricolaSchema


class AgroResources(Resource):
    def get(self):
        logger.info("GET request received for /agro endpoint")
        try:
            conn = get_conn()
            cursor = conn.cursor()
            statetment = "SELECT * FROM tb_agricola"
            cursor.execute(statetment)

            resultset = cursor.fetchall()

            agriculasResponse = []
            for row in resultset:
                cod_uf = row[0]
                cod_municipio = row[1]
                cod_distrito = row[2]
                cod_subdistrito = row[3]
                situacao = row[4]
                nom_tip_seglogr = row[5]
                nom_titulo_seglogr = row[6]
                nom_seglogr = row[7]
                num_endereco = row[8]
                desc_modificador = row[9]
                nom_comp_elem1 = row[10]
                val_comp_elem1 = row[11]
                nom_comp_elem2 = row[12]
                val_comp_elem2 = row[13]
                nom_comp_elem3 = row[14]
                val_comp_elem3 = row[15]
                nom_comp_elem4 = row[16]
                val_comp_elem4 = row[17]
                nom_comp_elem5 = row[18]
                val_comp_elem5 = row[19]
                latitude = row[20]
                longitude = row[21]
                altitude = row[22]
                desc_localidade = row[23]
                cod_especie = row[24]
                cep = row[25]

                agricola = Agricola(
                    cod_uf=cod_uf,
                    cod_municipio=cod_municipio,
                    cod_distrito=cod_distrito,
                    cod_subdistrito=cod_subdistrito,
                    situacao=situacao,
                    nom_tip_seglogr=nom_tip_seglogr,
                    nom_titulo_seglogr=nom_titulo_seglogr,
                    nom_seglogr=nom_seglogr,
                    num_endereco=num_endereco,
                    desc_modificador=desc_modificador,
                    nom_comp_elem1=nom_comp_elem1,
                    val_comp_elem1=val_comp_elem1,
                    nom_comp_elem2=nom_comp_elem2,
                    val_comp_elem2=val_comp_elem2,
                    nom_comp_elem3=nom_comp_elem3,
                    val_comp_elem3=val_comp_elem3,
                    nom_comp_elem4=nom_comp_elem4,
                    val_comp_elem4=val_comp_elem4,
                    nom_comp_elem5=nom_comp_elem5,
                    val_comp_elem5=val_comp_elem5,
                    latitude=latitude,
                    longitude=longitude,
                    altitude=altitude,
                    desc_localidade=desc_localidade,
                    cod_especie=cod_especie,
                    cep=cep
                )

                agriculasResponse.append(AgricolaSchema().dump(agricola))

            return agriculasResponse, 200

        except Error as e:
            logger.error(f"Database error occurred: {e}")
            return {"message": "An error occurred while fetching agricultural data."}, 500
