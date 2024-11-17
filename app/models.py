"""
Definição das classes de modelo para o sistema.
"""

class Usuario:
    """
    Classe que representa um usuário do sistema.
    """
    def __init__(self, id, nome, email, senha_hash, nivel_acesso, data_criacao, data_modificacao):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.nivel_acesso = nivel_acesso
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao

class Funcionario:
    """
    Classe que representa um funcionário.
    """
    def __init__(self, id, nome, sobrenome, cpf, cargo, salario, telefone, email, data_contratacao, data_criacao, data_modificacao):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.cargo = cargo
        self.salario = salario
        self.telefone = telefone
        self.email = email
        self.data_contratacao = data_contratacao
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao

class Cliente:
    """
    Classe que representa um cliente.
    """
    def __init__(self, id, nome, cpf_cnpj, telefone, email, data_criacao, data_modificacao):
        self.id = id
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.email = email
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao

class Produto:
    """
    Classe que representa um produto.
    """
    def __init__(self, id, nome, descricao, peso, preco, estoque, data_criacao, data_modificacao):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.peso = peso
        self.preco = preco
        self.estoque = estoque
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao

class Venda:
    """
    Classe que representa uma venda.
    """
    def __init__(self, id, data_venda, cliente_id, funcionario_id, produtos, valor_total, forma_pagamento, parcelas, frete, status, data_criacao, data_modificacao):
        self.id = id
        self.data_venda = data_venda
        self.cliente_id = cliente_id
        self.funcionario_id = funcionario_id
        self.produtos = produtos
        self.valor_total = valor_total
        self.forma_pagamento = forma_pagamento
        self.parcelas = parcelas
        self.frete = frete
        self.status = status
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao

class Despesa:
    """
    Classe que representa uma despesa.
    """
    def __init__(self, id, tipo, descricao, valor, data, beneficiario, data_criacao, data_modificacao):
        self.id = id
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.beneficiario = beneficiario
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao

class Plantio:
    """
    Classe que representa um plantio.
    """
    def __init__(self, id, data_plantio, tipo_cafe, hectares, localizacao, data_previsao_colheita, data_criacao, data_modificacao):
        self.id = id
        self.data_plantio = data_plantio
        self.tipo_cafe = tipo_cafe
        self.hectares = hectares
        self.localizacao = localizacao
        self.data_previsao_colheita = data_previsao_colheita
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao
