from Ingestao.origens import PathBasesComplementares
from Ingestao.EstadoCivil.inserir_dados_banco import DBEstadoCivil
from json import loads
import polars as pl


class IngestaoEstadoCivil:

    @staticmethod
    def obter_tabela_estado_civil():
        with open(PathBasesComplementares.ARQUIVO_ESTADO_CIVIL, 'r', encoding='utf-8') as arquivo_json:
            dados_estado_civil = loads(arquivo_json.read())

        return dados_estado_civil

    @staticmethod
    def dicionario_estado_civil(lista_estado_civil: list) -> dict:
        dict_estado_civil = {
            'ID_EC': [],
            'DSC_EC': []
        }
        for conjunto in lista_estado_civil:
            dict_estado_civil['ID_EC'].append(conjunto['ID_EC'])
            dict_estado_civil['DSC_EC'].append(conjunto['DSC_EC'])

        return dict_estado_civil

    @staticmethod
    def obter_ids_estado_civil(lista_estado_civil: list) -> tuple:
        tupla_ids = tuple([item['ID_EC'] for item in lista_estado_civil])

        return tupla_ids

    @staticmethod
    def dados_modificados(lista_estado_civil: list, tabela_banco: pl.DataFrame) -> list:
        lista_linhas = []
        for item in lista_estado_civil:
            for nm_coluna in tabela_banco.columns[1:]:
                dsc = tabela_banco.filter(pl.col('id_ec') == item[tabela_banco.columns[0].upper()])[nm_coluna].to_list()[0]
                if dsc == item[nm_coluna.upper()]:
                    print(f'{dsc} -> {item[nm_coluna.upper()]}')
                    lista_linhas.append(item)
        if lista_linhas:
            return lista_linhas
        else:
            return []

    @staticmethod
    def dados_novos(lista_estado_civil: list, tabela_banco: pl.DataFrame) -> list:
        novos_registros = []
        for item in lista_estado_civil:
            if item['ID_EC'] not in tabela_banco['id_ec'].unique().to_list():
                novos_registros.append(item)

        if novos_registros:
            return novos_registros
        else:
            return []


    def rotina(self):
        print('Obtendo dados da FOnte')
        lista_estado_civil = self.obter_tabela_estado_civil()

        print('Verificar te há atualizações no banco')
        tabela_completo = DBEstadoCivil().consultar_tb_estado_civil_completo()
        lista_estado_civil_atualizacao = self.dados_modificados(
            lista_estado_civil=lista_estado_civil,
            tabela_banco=tabela_completo
        )
        if lista_estado_civil_atualizacao:
            dicionario_dados_atualizados = self.dicionario_estado_civil(lista_estado_civil=lista_estado_civil_atualizacao)
            # criar metodo para atualizar os dados no banco

        lista_estado_civil_novos = self.dados_novos(
            lista_estado_civil=lista_estado_civil,
            tabela_banco=tabela_completo
        )
        if lista_estado_civil_novos:
            dicionario_dados_novos = self.dicionario_estado_civil(lista_estado_civil=lista_estado_civil_novos)
            DBEstadoCivil().inserir_tb_estado_civil(dicionario_dados=dicionario_dados_novos)

        print('Obtendo IDS dos registros já salvos em banco')
        ids = self.obter_ids_estado_civil(lista_estado_civil=lista_estado_civil)
        tabela = DBEstadoCivil().consultar_tb_estado_civil(tupla_ids=ids)

        return tabela

if __name__ == '__main__':
    pass

