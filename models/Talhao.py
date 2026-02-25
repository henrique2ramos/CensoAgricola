import uuid
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from helpers.database import db

class Talhao(db.Model):
    __tablename__ = 'talhoes'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    propriedade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(
        'propriedades.id', ondelete='CASCADE'), nullable=False)
    
    identificacao: Mapped[str] = mapped_column(String(255), nullable=False)
    area_cultivavel_ha: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    tipo_solo: Mapped[str] = mapped_column(String(100), nullable=True)

    def __init__(self, propriedade_id, identificacao, area_cultivavel_ha, tipo_solo=None):
        self.propriedade_id = propriedade_id
        self.identificacao = identificacao
        self.area_cultivavel_ha = area_cultivavel_ha
        self.tipo_solo = tipo_solo

    def __repr__(self):
        return f"<Talhao(id={self.id}, identificacao='{self.identificacao}')>"
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'propriedade_id': str(self.propriedade_id),
            'identificacao': self.identificacao,
            'area_cultivavel_ha': float(self.area_cultivavel_ha),
            'tipo_solo': self.tipo_solo
        }


class TalhaoSchema(Schema):
    id = fields.UUID(dump_only=True)
    propriedade_id = fields.UUID(required=True)
    identificacao = fields.Str(required=True, validate=validate.Length(max=255))
    area_cultivavel_ha = fields.Float(required=True)
    tipo_solo = fields.Str(validate=validate.Length(max=100), allow_none=True)
