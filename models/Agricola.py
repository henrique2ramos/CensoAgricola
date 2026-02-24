from marshmallow import Schema, fields, validate
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Text

from helpers.database import db


class Agricola():

    __tablename__ = 'tb_agricola'

    cod_uf: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_municipio: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_distrito: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_subdistrito: Mapped[int] = mapped_column(Integer, primary_key=True)
    situacao: Mapped[str] = mapped_column(String(1))
    nom_tip_seglogr: Mapped[str] = mapped_column(String(50))
    nom_titulo_seglogr: Mapped[str] = mapped_column(String(50))
    nom_seglogr: Mapped[str] = mapped_column(String(100))
    num_endereco: Mapped[str] = mapped_column(String(20))
    dsc_modificador: Mapped[str] = mapped_column(String(50))
    nom_comp_elem1: Mapped[str] = mapped_column(String(50))
    val_comp_elem1: Mapped[str] = mapped_column(String(50))
    nom_comp_elem2: Mapped[str] = mapped_column(String(50))
    val_comp_elem2: Mapped[str] = mapped_column(String(50))
    nom_comp_elem3: Mapped[str] = mapped_column(String(50))
    val_comp_elem3: Mapped[str] = mapped_column(String(50))
    nom_comp_elem4: Mapped[str] = mapped_column(String(50))
    val_comp_elem4: Mapped[str] = mapped_column(String(50))
    nom_comp_elem5: Mapped[str] = mapped_column(String(50))
    val_comp_elem5: Mapped[str] = mapped_column(String(50))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    altitude: Mapped[float] = mapped_column(Float)
    desc_localidade: Mapped[str] = mapped_column(String(100))
    cod_especie: Mapped[int] = mapped_column(Integer)
    cep: Mapped[str] = mapped_column(String(20))

    def __init__(self, cod_uf, cod_municipio, cod_distrito, cod_subdistrito, situacao, nom_tip_seglogr, nom_titulo_seglogr, nom_seglogr, num_endereco, desc_modificador, nom_comp_elem1, val_comp_elem1, nom_comp_elem2, val_comp_elem2, nom_comp_elem3, val_comp_elem3, nom_comp_elem4, val_comp_elem4, nom_comp_elem5, val_comp_elem5, latitude, longitude, altitude, desc_localidade, cod_especie, cep):
        self.cod_uf = cod_uf
        self.cod_municipio = cod_municipio
        self.cod_distrito = cod_distrito
        self.cod_subdistrito = cod_subdistrito
        self.situacao = situacao
        self.nom_tip_seglogr = nom_tip_seglogr
        self.nom_titulo_seglogr = nom_titulo_seglogr
        self.nom_seglogr = nom_seglogr
        self.num_endereco = num_endereco
        self.dsc_modificador = desc_modificador
        self.nom_comp_elem1 = nom_comp_elem1
        self.val_comp_elem1 = val_comp_elem1
        self.nom_comp_elem2 = nom_comp_elem2
        self.val_comp_elem2 = val_comp_elem2
        self.nom_comp_elem3 = nom_comp_elem3
        self.val_comp_elem3 = val_comp_elem3
        self.nom_comp_elem4 = nom_comp_elem4
        self.val_comp_elem4 = val_comp_elem4
        self.nom_comp_elem5 = nom_comp_elem5
        self.val_comp_elem5 = val_comp_elem5
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.desc_localidade = desc_localidade
        self.cod_especie = cod_especie
        self.cep = cep

    def __repr__(self):
        return f'<Agricola {self.cod_uf} - {self.cod_municipio} - {self.cod_distrito} - {self.cod_subdistrito}>'

    def to_json(self):
        return {
            "cod_uf": self.cod_uf,
            "cod_municipio": self.cod_municipio,
            "cod_distrito": self.cod_distrito,
            "cod_subdistrito": self.cod_subdistrito,
            "situacao": self.situacao,
            "nom_tip_seglogr": self.nom_tip_seglogr,
            "nom_titulo_seglogr": self.nom_titulo_seglogr,
            "nom_seglogr": self.nom_seglogr,
            "num_endereco": self.num_endereco,
            "dsc_modificador": self.dsc_modificador,
            "nom_comp_elem1": self.nom_comp_elem1,
            "val_comp_elem1": self.val_comp_elem1,
            "nom_comp_elem2": self.nom_comp_elem2,
            "val_comp_elem2": self.val_comp_elem2,
            "nom_comp_elem3": self.nom_comp_elem3,
            "val_comp_elem3": self.val_comp_elem3,
            "nom_comp_elem4": self.nom_comp_elem4,
            "val_comp_elem4": self.val_comp_elem4,
            "nom_comp_elem5": self.nom_comp_elem5,
            "val_comp_elem5": self.val_comp_elem5,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "desc_localidade": self.desc_localidade,
            "cod_especie": self.cod_especie,
            "cep": self.cep
        }


class AgricolaSchema(Schema):
    cod_uf = fields.Int(required=True)
    cod_municipio = fields.Int(required=True)
    cod_distrito = fields.Int(required=True)
    cod_subdistrito = fields.Int(required=True)
    situacao = fields.Str(required=True, validate=validate.Length(max=1))
    nom_tip_seglogr = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_titulo_seglogr = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_seglogr = fields.Str(required=True, validate=validate.Length(max=100))
    num_endereco = fields.Str(required=True, validate=validate.Length(max=20))
    dsc_modificador = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_comp_elem1 = fields.Str(
        required=True, validate=validate.Length(max=50))
    val_comp_elem1 = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_comp_elem2 = fields.Str(
        required=True, validate=validate.Length(max=50))
    val_comp_elem2 = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_comp_elem3 = fields.Str(
        required=True, validate=validate.Length(max=50))
    val_comp_elem3 = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_comp_elem4 = fields.Str(
        required=True, validate=validate.Length(max=50))
    val_comp_elem4 = fields.Str(
        required=True, validate=validate.Length(max=50))
    nom_comp_elem5 = fields.Str(
        required=True, validate=validate.Length(max=50))
    val_comp_elem5 = fields.Str(
        required=True, validate=validate.Length(max=50))
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    altitude = fields.Float(required=True)
    desc_localidade = fields.Str(
        required=True, validate=validate.Length(max=100))
    cod_especie = fields.Int(required=True)
    cep = fields.Str(required=True, validate=validate.Length(max=20))


if __name__ == "__main__":
    agricola = Agricola(
        cod_uf=1,
        cod_municipio=1,
        cod_distrito=1,
        cod_subdistrito=1,
        situacao='A',
        nom_tip_seglogr='Rua',
        nom_titulo_seglogr='Rua Principal',
        nom_seglogr='Rua Principal',
        num_endereco='123',
        desc_modificador='Nenhum',
        nom_comp_elem1='Complemento 1',
        val_comp_elem1='Valor 1',
        nom_comp_elem2='Complemento 2',
        val_comp_elem2='Valor 2',
        nom_comp_elem3='Complemento 3',
        val_comp_elem3='Valor 3',
        nom_comp_elem4='Complemento 4',
        val_comp_elem4='Valor 4',
        nom_comp_elem5='Complemento 5',
        val_comp_elem5='Valor 5',
        latitude=-23.55052,
        longitude=-46.633308,
        altitude=760.0,
        desc_localidade='São Paulo',
        cod_especie=1,
        cep='01000-000'
    )

    print(agricola.to_json())
