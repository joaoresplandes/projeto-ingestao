import requests
from MongoDB.rotina import RotinaMongo
from pprint import pprint


# @staticmethod
# def verificar_items_ufs(requisicao: dict, mongo_db: dict):
#     print(requisicao)

response = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/estados')
resposta = response.json()

dicionario_regiao = {}

for item in resposta:
    dicionario_regiao[item['sigla']] = {
        'nm_uf': item['nome'],
        'regiao_sigla': item["regiao"]['nome'],
        'regiao': item['regiao']['nome']
    }

# dicionario_ufs = {'UFS': dicionario_regiao}
pprint(dicionario_regiao)
print('-'*100)
# RotinaMongo().inserir_ufs(dicionario_regiao)
ufs_banco = RotinaMongo().listar_ufs()
ufs_banco = {list(uf)[1]: uf[list(uf)[1]] for uf in ufs_banco}


print(ufs_banco)



