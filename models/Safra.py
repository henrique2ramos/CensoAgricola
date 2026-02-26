from marshmallow import Schema, fields, validate
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey, Integer
from helpers.database import db


class Safra(db.Model):
    __tablename__ = 'safras'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    talhao_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'talhoes.id', ondelete='CASCADE'), nullable=False)

    cultura: Mapped[str] = mapped_column(String(255), nullable=False)
    variedade: Mapped[str] = mapped_column(String(255), nullable=True)
    data_plantio_estimada: Mapped[str] = mapped_column(
        String(255), nullable=True)
    data_colheita_estimada: Mapped[str] = mapped_column(
        String(255), nullable=True)
    expectativa_producao: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=True)

    def __init__(self, talhao_id, cultura, variedade=None, data_plantio_estimada=None,
                 data_colheita_estimada=None, expectativa_producao=None):
        self.talhao_id = talhao_id
        self.cultura = cultura
        self.variedade = variedade
        self.data_plantio_estimada = data_plantio_estimada
        self.data_colheita_estimada = data_colheita_estimada
        self.expectativa_producao = expectativa_producao

    def __repr__(self):
        return f"<Safra(id={self.id}, cultura='{self.cultura}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'talhao_id': self.talhao_id,
            'cultura': self.cultura,
            'variedade': self.variedade,
            'data_plantio_estimada': self.data_plantio_estimada,
            'data_colheita_estimada': self.data_colheita_estimada,
            'expectativa_producao': float(self.expectativa_producao) if self.expectativa_producao is not None else None
        }


class SafraSchema(Schema):
    id = fields.Int(dump_only=True)
    talhao_id = fields.Int(required=True)
    cultura = fields.Str(required=True, validate=validate.Length(max=255))
    variedade = fields.Str(validate=validate.Length(max=255), allow_none=True)
    data_plantio_estimada = fields.Str(
        validate=validate.Length(max=255), allow_none=True)
    data_colheita_estimada = fields.Str(
        validate=validate.Length(max=255), allow_none=True)
    expectativa_producao = fields.Float(allow_none=True)
