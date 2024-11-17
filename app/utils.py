"""
Funções utilitárias para interação com o Google Sheets.
"""

import os
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS_PATH = os.path.join('credentials', 'credentials.json')
SHEET_ID = os.environ.get('SHEET_ID')

def get_service():
    """Obtém o serviço da API do Google Sheets."""
    creds = service_account.Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def read_sheet(range_name):
    """Lê os dados de uma planilha."""
    service = get_service()
    try:
        result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=range_name).execute()
        values = result.get('values', [])
        return values
    except HttpError as err:
        print(err)
        return None

def write_sheet(range_name, values):
    """Escreve dados em uma planilha."""
    service = get_service()
    body = {
        'values': values
    }
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=range_name,
            valueInputOption='RAW', body=body).execute()
        return result
    except HttpError as err:
        print(err)
        return None

def append_sheet(range_name, values):
    """Anexa dados ao final de uma planilha."""
    service = get_service()
    body = {
        'values': values
    }
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID, range=range_name,
            valueInputOption='RAW', body=body,
            insertDataOption='INSERT_ROWS').execute()
        return result
    except HttpError as err:
        print(err)
        return None

def update_row(range_name, values):
    """Atualiza uma linha específica em uma planilha."""
    return write_sheet(range_name, values)

def delete_row(sheet_id, row_number):
    """Exclui uma linha de uma planilha."""
    service = get_service()
    requests = [{
        'deleteDimension': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': row_number,
                'endIndex': row_number + 1
            }
        }
    }]
    body = {'requests': requests}
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID, body=body).execute()
        return response
    except HttpError as err:
        print(err)
        return None

def get_sheet_id_by_name(sheet_name):
    """Obtém o ID da aba da planilha pelo nome."""
    service = get_service()
    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheets = spreadsheet.get('sheets', '')
        for sheet in sheets:
            if sheet.get("properties", {}).get("title", "") == sheet_name:
                return sheet.get("properties", {}).get("sheetId", 0)
        return None
    except HttpError as err:
        print(err)
        return None

# Funções para Usuários
def get_usuarios():
    """Obtém a lista de usuários."""
    values = read_sheet('Usuarios!A1:G')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.to_dict('records')

def save_usuario(usuario):
    """Salva um novo usuário."""
    values = [[
        usuario['id'],
        usuario['nome'],
        usuario['email'],
        usuario['senha_hash'],
        usuario['nivel_acesso'],
        usuario['data_criacao'],
        usuario['data_modificacao']
    ]]
    append_sheet('Usuarios!A1', values)

def update_usuario(id, usuario):
    """
    Atualiza um usuário existente na planilha.

    Args:
        id (int): ID do usuário a ser atualizado.
        usuario (dict): Dados do usuário atualizados.
    """
    usuarios = get_usuarios()
    index = next((i for i, u in enumerate(usuarios) if int(u['id']) == id), None)
    if index is not None:
        range_name = f'Usuarios!A{index + 2}:G{index + 2}'  # +2 para considerar cabeçalho e índice zero
        values = [[
            usuario.get('id', usuarios[index]['id']),
            usuario.get('nome', usuarios[index]['nome']),
            usuario.get('email', usuarios[index]['email']),
            usuario.get('senha_hash', usuarios[index]['senha_hash']),
            usuario.get('nivel_acesso', usuarios[index]['nivel_acesso']),
            usuarios[index]['data_criacao'],
            datetime.utcnow().isoformat()  # Atualiza a data de modificação
        ]]
        return update_row(range_name, values)
    else:
        return None

def delete_usuario(id):
    """
    Exclui um usuário existente na planilha.

    Args:
        id (int): ID do usuário a ser excluído.
    """
    usuarios = get_usuarios()
    index = next((i for i, u in enumerate(usuarios) if int(u['id']) == id), None)
    if index is not None:
        sheet_id = get_sheet_id_by_name('Usuarios')
        return delete_row(sheet_id, index + 1)  # +1 para considerar cabeçalho
    else:
        return None

# Funções para Funcionários
def get_funcionarios():
    """Obtém a lista de funcionários."""
    values = read_sheet('Funcionarios!A1:K')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.to_dict('records')

def save_funcionario(funcionario):
    """Salva um novo funcionário."""
    values = [[
        funcionario['id'],
        funcionario['nome'],
        funcionario['sobrenome'],
        funcionario['cpf'],
        funcionario['cargo'],
        funcionario['salario'],
        funcionario['telefone'],
        funcionario['email'],
        funcionario['data_contratacao'],
        funcionario['data_criacao'],
        funcionario['data_modificacao']
    ]]
    append_sheet('Funcionarios!A1', values)

def update_funcionario(index, funcionario):
    """Atualiza um funcionário existente."""
    range_name = f'Funcionarios!A{index + 2}:K{index + 2}'
    values = [[
        funcionario.get('id', funcionario['id']),
        funcionario.get('nome', funcionario['nome']),
        funcionario.get('sobrenome', funcionario['sobrenome']),
        funcionario.get('cpf', funcionario['cpf']),
        funcionario.get('cargo', funcionario['cargo']),
        funcionario.get('salario', funcionario['salario']),
        funcionario.get('telefone', funcionario['telefone']),
        funcionario.get('email', funcionario['email']),
        funcionario.get('data_contratacao', funcionario['data_contratacao']),
        funcionario.get('data_criacao', funcionario['data_criacao']),
        funcionario.get('data_modificacao', funcionario['data_modificacao'])
    ]]
    update_row(range_name, values)

def delete_funcionario(index):
    """Exclui um funcionário."""
    sheet_id = get_sheet_id_by_name('Funcionarios')
    delete_row(sheet_id, index + 1)  # +1 por causa do cabeçalho

# Funções para Clientes
def get_clientes():
    """Obtém a lista de clientes."""
    values = read_sheet('Clientes!A1:G')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.to_dict('records')

def save_cliente(cliente):
    """Salva um novo cliente."""
    values = [[
        cliente['id'],
        cliente['nome'],
        cliente['cpf_cnpj'],
        cliente['telefone'],
        cliente['email'],
        cliente['data_criacao'],
        cliente['data_modificacao']
    ]]
    append_sheet('Clientes!A1', values)

def update_cliente(index, cliente):
    """Atualiza um cliente existente."""
    range_name = f'Clientes!A{index + 2}:G{index + 2}'
    values = [[
        cliente.get('id', cliente['id']),
        cliente.get('nome', cliente['nome']),
        cliente.get('cpf_cnpj', cliente['cpf_cnpj']),
        cliente.get('telefone', cliente['telefone']),
        cliente.get('email', cliente['email']),
        cliente.get('data_criacao', cliente['data_criacao']),
        datetime.utcnow().isoformat()  # Atualiza a data de modificação
    ]]
    update_row(range_name, values)

def delete_cliente(index):
    """Exclui um cliente."""
    sheet_id = get_sheet_id_by_name('Clientes')
    delete_row(sheet_id, index + 1)  # +1 por causa do cabeçalho

# Funções para Produtos
def get_produtos():
    """Obtém a lista de produtos."""
    values = read_sheet('Produtos!A1:H')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.to_dict('records')

def save_produto(produto):
    """Salva um novo produto."""
    values = [[
        produto['id'],
        produto['nome'],
        produto['descricao'],
        produto['peso'],
        produto['preco'],
        produto['estoque'],
        produto['data_criacao'],
        produto['data_modificacao']
    ]]
    append_sheet('Produtos!A1', values)

def update_produto(index, produto):
    """Atualiza um produto existente."""
    range_name = f'Produtos!A{index + 2}:H{index + 2}'
    values = [[
        produto.get('id', produto['id']),
        produto.get('nome', produto['nome']),
        produto.get('descricao', produto['descricao']),
        produto.get('peso', produto['peso']),
        produto.get('preco', produto['preco']),
        produto.get('estoque', produto['estoque']),
        produto.get('data_criacao', produto['data_criacao']),
        datetime.utcnow().isoformat()  # Atualiza a data de modificação
    ]]
    update_row(range_name, values)

def delete_produto(index):
    """Exclui um produto."""
    sheet_id = get_sheet_id_by_name('Produtos')
    delete_row(sheet_id, index + 1)  # +1 por causa do cabeçalho

# Funções para Vendas
def get_vendas():
    """Obtém a lista de vendas."""
    values = read_sheet('Vendas!A1:L')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    # Converter produtos de string para dict
    df['produtos'] = df['produtos'].apply(json.loads)
    return df.to_dict('records')

def save_venda(venda):
    """Salva uma nova venda."""
    values = [[
        venda['id'],
        venda['data_venda'],
        venda['cliente_id'],
        venda['funcionario_id'],
        json.dumps(venda['produtos']),
        venda['valor_total'],
        venda['forma_pagamento'],
        venda['parcelas'],
        venda['frete'],
        venda['status'],
        venda['data_criacao'],
        venda['data_modificacao']
    ]]
    append_sheet('Vendas!A1', values)

def update_venda(index, venda):
    """Atualiza uma venda existente."""
    range_name = f'Vendas!A{index + 2}:L{index + 2}'
    values = [[
        venda.get('id', venda['id']),
        venda.get('data_venda', venda['data_venda']),
        venda.get('cliente_id', venda['cliente_id']),
        venda.get('funcionario_id', venda['funcionario_id']),
        json.dumps(venda.get('produtos', venda['produtos'])),
        venda.get('valor_total', venda['valor_total']),
        venda.get('forma_pagamento', venda['forma_pagamento']),
        venda.get('parcelas', venda['parcelas']),
        venda.get('frete', venda['frete']),
        venda.get('status', venda['status']),
        venda.get('data_criacao', venda['data_criacao']),
        venda.get('data_modificacao', venda['data_modificacao'])
    ]]
    update_row(range_name, values)

def delete_venda(index):
    """Exclui uma venda."""
    sheet_id = get_sheet_id_by_name('Vendas')
    delete_row(sheet_id, index + 1)  # +1 por causa do cabeçalho

# Funções para Despesas
def get_despesas():
    """Obtém a lista de despesas."""
    values = read_sheet('Despesas!A1:H')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.to_dict('records')

def save_despesa(despesa):
    """Salva uma nova despesa."""
    values = [[
        despesa['id'],
        despesa['tipo'],
        despesa['descricao'],
        despesa['valor'],
        despesa['data'],
        despesa['beneficiario'],
        despesa['data_criacao'],
        despesa['data_modificacao']
    ]]
    append_sheet('Despesas!A1', values)

def update_despesa(index, despesa):
    """Atualiza uma despesa existente."""
    range_name = f'Despesas!A{index + 2}:H{index + 2}'
    values = [[
        despesa.get('id', despesa['id']),
        despesa.get('tipo', despesa['tipo']),
        despesa.get('descricao', despesa['descricao']),
        despesa.get('valor', despesa['valor']),
        despesa.get('data', despesa['data']),
        despesa.get('beneficiario', despesa['beneficiario']),
        despesa.get('data_criacao', despesa['data_criacao']),
        datetime.utcnow().isoformat()  # Atualiza a data de modificação
    ]]
    update_row(range_name, values)

def delete_despesa(index):
    """Exclui uma despesa."""
    sheet_id = get_sheet_id_by_name('Despesas')
    delete_row(sheet_id, index + 1)  # +1 por causa do cabeçalho

# Funções para Plantios
def get_plantios():
    """Obtém a lista de plantios."""
    values = read_sheet('Plantios!A1:H')
    if not values:
        return []
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.to_dict('records')

def save_plantio(plantio):
    """Salva um novo plantio."""
    values = [[
        plantio['id'],
        plantio['data_plantio'],
        plantio['tipo_cafe'],
        plantio['hectares'],
        plantio['localizacao'],
        plantio['data_previsao_colheita'],
        plantio['data_criacao'],
        plantio['data_modificacao']
    ]]
    append_sheet('Plantios!A1', values)

def update_plantio(index, plantio):
    """Atualiza um plantio existente."""
    range_name = f'Plantios!A{index + 2}:H{index + 2}'
    values = [[
        plantio.get('id', plantio['id']),
        plantio.get('data_plantio', plantio['data_plantio']),
        plantio.get('tipo_cafe', plantio['tipo_cafe']),
        plantio.get('hectares', plantio['hectares']),
        plantio.get('localizacao', plantio['localizacao']),
        plantio.get('data_previsao_colheita', plantio['data_previsao_colheita']),
        plantio.get('data_criacao', plantio['data_criacao']),
        datetime.utcnow().isoformat()  # Atualiza a data de modificação
    ]]
    update_row(range_name, values)

def delete_plantio(index):
    """Exclui um plantio."""
    sheet_id = get_sheet_id_by_name('Plantios')
    delete_row(sheet_id, index + 1)  # +1 por causa do cabeçalho
