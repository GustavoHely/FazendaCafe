"""
Rotas relacionadas aos relatórios.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils import get_vendas, get_despesas
from datetime import datetime

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/financeiro', methods=['GET'])
@jwt_required()
def relatorio_financeiro():
    """
    Gera um relatório financeiro com base nas vendas e despesas.
    """
    data_inicio = request.args.get('data_inicio')  # Formato: YYYY-MM-DD
    data_fim = request.args.get('data_fim')        # Formato: YYYY-MM-DD

    vendas = get_vendas()
    despesas = get_despesas()

    # Filtrar por data
    if data_inicio:
        vendas = [v for v in vendas if v['data_venda'] >= data_inicio]
        despesas = [d for d in despesas if d['data'] >= data_inicio]

    if data_fim:
        vendas = [v for v in vendas if v['data_venda'] <= data_fim]
        despesas = [d for d in despesas if d['data'] <= data_fim]

    total_vendas = sum(float(v['valor_total']) for v in vendas)
    total_despesas = sum(float(d['valor']) for d in despesas)
    lucro = total_vendas - total_despesas

    relatorio = {
        'total_vendas': total_vendas,
        'total_despesas': total_despesas,
        'lucro': lucro,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }

    return jsonify(relatorio), 200
