from marshmallow import Schema, fields, validate
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey, Integer
from helpers.database import db


class Propriedade(db.Model):
    __tablename__ = 'propriedades'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    produtor_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'produtores.id', ondelete='CASCADE'), nullable=False)

    nome_propriedade: Mapped[str] = mapped_column(String(255), nullable=False)
    numero_car: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=True)
    numero_ccir: Mapped[str] = mapped_column(String(50), nullable=True)
    codigo_municipio: Mapped[str] = mapped_column(String(7), nullable=True)
    codigo_uf: Mapped[str] = mapped_column(String(2), nullable=True)

    area_total_ha: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False)
    area_preservacao_ha: Mapped[float] = mapped_column(
        Numeric(12, 2), default=0.0)
    area_infraestrutura_ha: Mapped[float] = mapped_column(
        Numeric(12, 2), default=0.0)

    latitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)

    def __init__(self, produtor_id, nome_propriedade, area_total_ha, numero_car=None,
                 numero_ccir=None, codigo_municipio=None, codigo_uf=None, area_preservacao_ha=0.0,
                 area_infraestrutura_ha=0.0, latitude=None, longitude=None):
        self.produtor_id = produtor_id
        self.nome_propriedade = nome_propriedade
        self.area_total_ha = area_total_ha
        self.numero_car = numero_car
        self.numero_ccir = numero_ccir
        self.codigo_municipio = codigo_municipio
        self.codigo_uf = codigo_uf
        self.area_preservacao_ha = area_preservacao_ha
        self.area_infraestrutura_ha = area_infraestrutura_ha
        self.latitude = latitude
        self.longitude = longitude


class PropriedadeSchema(Schema):
    id = fields.Int(dump_only=True)
    produtor_id = fields.Int(required=True)
    nome_propriedade = fields.Str(
        required=True, validate=validate.Length(max=255))
    numero_car = fields.Str(validate=validate.Length(max=100), allow_none=True)
    numero_ccir = fields.Str(validate=validate.Length(max=50), allow_none=True)
    codigo_municipio = fields.Str(validate=validate.Length(equal=7), allow_none=True)
    codigo_uf = fields.Str(validate=validate.Length(equal=2), allow_none=True)
    codigo_ue = fields.Str(load_only=True, validate=validate.Length(equal=2), allow_none=True)

    area_total_ha = fields.Float(required=True)
    area_preservacao_ha = fields.Float(dump_default=0.0, load_default=0.0)
    area_infraestrutura_ha = fields.Float(dump_default=0.0, load_default=0.0)

    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
