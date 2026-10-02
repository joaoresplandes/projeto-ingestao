from Pipeline.Bronze.MongoDB.rotina import RotinaMongo
from Pipeline.Bronze.MongoDB.comum import ComumMongo
import requests
from datetime import datetime
import json
from pprint import pprint


@staticmethod
def verificar_items_ufs(requisicao: dict, mongo_db: dict):
    print(requisicao)

response = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/estados')
resposta = response.json()

dicionario_regiao = {}
for item in resposta:
    dicionario_regiao[item['sigla']] = {
        'nm_uf': item['nome'],
        'regiao_sigla': item["regiao"]['sigla'],
        'regiao': item['regiao']['nome'],
        'data_insercao': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

pprint(dicionario_regiao)
print('-'*100)
# RotinaMongo().inserir_ufs(dicionario_regiao)
ufs_banco = RotinaMongo().listar_ufs()
ufs_banco = {list(uf)[1]: uf[list(uf)[1]] for uf in ufs_banco}
pprint(ufs_banco)
print('-' * 100)

dicionario_verificacao = {}
for uf in dicionario_regiao:
    lista_status_atual = []
    dicionario_verificacao[uf] = {'status': {}}
    for chave in list(dicionario_regiao[uf].keys())[:-1]:
        if dicionario_regiao[uf][chave] == ufs_banco[uf][chave]:
            lista_status_atual.append(True)
        else:
            lista_status_atual.append(False)
        dicionario_verificacao[uf].update(
            {'status':True if True in list(set(lista_status_atual)) else False}
        )
pprint(dicionario_verificacao)
