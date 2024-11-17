"""
Definição dos schemas para serialização e deserialização.
"""

from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    """Schema para a classe Usuario."""
    id = fields.Int()
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(load_only=True)
    senha_hash = fields.Str(dump_only=True)
    nivel_acesso = fields.Str(required=True)
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()

class FuncionarioSchema(Schema):
    """Schema para a classe Funcionario."""
    id = fields.Int()
    nome = fields.Str(required=True)
    sobrenome = fields.Str(required=True)
    cpf = fields.Str(required=True)
    cargo = fields.Str(required=True)
    salario = fields.Float(required=True)
    telefone = fields.Str()
    email = fields.Email()
    data_contratacao = fields.Date()
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()

class ClienteSchema(Schema):
    """Schema para a classe Cliente."""
    id = fields.Int()
    nome = fields.Str(required=True)
    cpf_cnpj = fields.Str(required=True)
    telefone = fields.Str()
    email = fields.Email()
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()

class ProdutoSchema(Schema):
    """Schema para a classe Produto."""
    id = fields.Int()
    nome = fields.Str(required=True)
    descricao = fields.Str()
    peso = fields.Float()
    preco = fields.Float(required=True)
    estoque = fields.Int()
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()

class VendaSchema(Schema):
    """Schema para a classe Venda."""
    id = fields.Int()
    data_venda = fields.DateTime()
    cliente_id = fields.Int(required=True)
    funcionario_id = fields.Int()
    produtos = fields.List(fields.Dict())
    valor_total = fields.Float()
    forma_pagamento = fields.Str()
    parcelas = fields.Int()
    frete = fields.Float()
    status = fields.Str()
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()

class DespesaSchema(Schema):
    """Schema para a classe Despesa."""
    id = fields.Int()
    tipo = fields.Str(required=True)
    descricao = fields.Str()
    valor = fields.Float(required=True)
    data = fields.Date()
    beneficiario = fields.Str()
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()

class PlantioSchema(Schema):
    """Schema para a classe Plantio."""
    id = fields.Int()
    data_plantio = fields.Date()
    tipo_cafe = fields.Str(required=True)
    hectares = fields.Float(required=True)
    localizacao = fields.Str()
    data_previsao_colheita = fields.Date()
    data_criacao = fields.DateTime()
    data_modificacao = fields.DateTime()
