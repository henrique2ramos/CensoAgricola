from datetime import datetime
from marshmallow import Schema, fields, validate
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from helpers.database import db


class Produtor(db.Model):
    __tablename__ = 'produtores'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    nome_razao_social: Mapped[str] = mapped_column(String(255), nullable=False)
    documento: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    inscricao_estadual: Mapped[str] = mapped_column(String(255), nullable=True)
    tipo_vinculo: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())

    def __init__(self, nome_razao_social, documento, tipo_vinculo,
                 inscricao_estadual=None, telefone=None, email=None):
        self.nome_razao_social = nome_razao_social
        self.documento = documento
        self.tipo_vinculo = tipo_vinculo
        self.inscricao_estadual = inscricao_estadual
        self.telefone = telefone
        self.email = email

    def __repr__(self):
        return f"<Produtor(id={self.id}, nome='{self.nome_razao_social}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'nome_razao_social': self.nome_razao_social,
            'documento': self.documento,
            'inscricao_estadual': self.inscricao_estadual,
            'tipo_vinculo': self.tipo_vinculo,
            'telefone': self.telefone,
            'email': self.email,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }


class ProdutorSchema(Schema):
    id = fields.Int(dump_only=True)
    nome_razao_social = fields.Str(
        required=True, validate=validate.Length(max=255))
    documento = fields.Str(required=True, validate=validate.Length(max=255))
    inscricao_estadual = fields.Str(
        validate=validate.Length(max=255), allow_none=True)
    tipo_vinculo = fields.Str(required=True, validate=validate.Length(max=255))
    telefone = fields.Str(validate=validate.Length(max=255), allow_none=True)
    email = fields.Email(validate=validate.Length(max=255), allow_none=True)
    criado_em = fields.DateTime(dump_only=True)
