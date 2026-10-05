from Pipeline.Silver.SIS_CRM_CHURN.fluxo_db_sis_crm_churn import DBCrmChur
from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
from Pipeline.Silver.Ingestao.ingestao import CamadaBronze
from unidecode import unidecode
import polars as pl
import re


class SilverSisCrmChurn(RotinaBanco):
    def __init__(self):

        self.__nm_tabela_churn_bronze = CamadaBronze().tb_sis_crm_churn_bronze()
        self.__nm_tabela_churn_silver = 'projeto_churn.silver.tb_sis_crm_churn'
        self._mapeamento = {
            r'\b(masculino|masc|m)\b': 'M',
            r'\b(bigenero|bi|b)\b': 'B',
            r'\b(feminino|fem|fe|f)\b': 'F',
            r'\b(agenero|ag|a)\b': 'A',
            r'\b(outros|outro|o)\b': 'O'
        }
        super().__init__(nome_tabela=self.__nm_tabela_churn_silver)

    @property
    def tabela_completa(self):
        return self.__nm_tabela_churn_bronze

    def transformar_dataframe_dicionario(self) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela = self.__nm_tabela_churn_bronze
        tabela_temp = tabela.with_columns(pl.Series([index for index in range(tabela.shape[0])]).alias('index'))
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela.columns[:-1]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados

    def tratar_genero(self, texto: str) -> str:
        """
        Com uma função regex, reconhece o padrão no valor de cada linha da coluna e retorna o valor correspondente de
        mapeamento
        :param texto: texto a ser compradado -> coluna genero
        :return: M, B, F, A, O
        """
        texto = unidecode(texto).lower()
        for padrao, valor in self._mapeamento.items():
            texto = re.sub(padrao, valor, texto, flags=re.IGNORECASE | re.VERBOSE)
        return texto

    def tratar_colunas(self, list_dict_tabela: list) -> list:
        """
        Tratando cada uma das respectivas decolunas de acordo com cada especialidade:
        1° CPF -> Retirar '.' e '-'
        2° GENERO -> Usa ReGex para encontrar um padrão no texto e retonar a categoria correta
        3° ID -> Transforma o tipo de dados que antes era String para Int
        4° IndCliente -> Transforma o valor que antes era String para Int e caso encontre um valor Null, converte
        para 0 (Zero)
        :param list_dict_tabela: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return:dicionario de dados ja estruturado tratado
        """
        list_dict_tabela_saida = []
        for dict_tabela in list_dict_tabela:
            dict_tabela['id'] = int(dict_tabela['id'])
            dict_tabela['cpf'] = int(dict_tabela['cpf'].replace('.', '').replace('-', ''))
            dict_tabela['idgenero'] = self.tratar_genero(texto=dict_tabela['idgenero'])
            dict_tabela['estado_civil'] = int(dict_tabela['estado_civil'])
            dict_tabela['idade'] = int(dict_tabela['idade'])
            dict_tabela['escolaridade'] = int(dict_tabela['escolaridade'])
            dict_tabela['indcliente'] = int(dict_tabela['indcliente']) if dict_tabela['indcliente'] != '' else 0

            list_dict_tabela_saida.append(dict_tabela)

        return list_dict_tabela_saida

    @staticmethod
    def obter_ids_bronze(lista_dicionario_dados: list) -> list:
        """
        Retorna uma lista de ids da tabela crm churn proveniente da camana bronze
        :param lista_dicionario_dados: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...]
        """
        lista_ids_bronze = [dicionario['id'] for dicionario in lista_dicionario_dados]
        
        return lista_ids_bronze

    @staticmethod
    def comparar_ids_entre_camadas(ids_bronze: list, ids_silver) -> tuple[list, list]:
        """
        Verifica se na camada Bronze tem novos registros que ainda não contem na cama Silver
        :param ids_bronze: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...]
        :param ids_silver: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...]
        :return: [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, ...]
        """
        ids_novos = [
            id_bronze for id_bronze in ids_bronze
            if int(id_bronze) not in [int(num_id) for num_id in [int(id) for id in ids_silver]]
        ]

        ids_existentes = [
            id_bronze for id_bronze in ids_bronze
            if int(id_bronze) in [int(num_id) for num_id in [int(id) for id in ids_silver]]
        ]

        return ids_novos, ids_existentes

    @staticmethod
    def filtrar_dados(lista_ids: list, dados_camada_bronze: list) -> list:
        """
        Com a lista de ids novos, é possivel filtrar apenas os registros novos da lista de dicionario de dados para
        serem encaminhados para a camada Silver
        :param lista_ids: [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, ...]
        :param dados_camada_bronze: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': 33, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        dados_novos = [dado for dado in dados_camada_bronze if int(dado['id']) in [int(id) for id in lista_ids]]

        return dados_novos

    def verifica_dados_atualizados(self, dados_sis_crm_churn: list) -> list:
        """
        Verifica se os dados de 'dados_sis_crm_churn' contem no banco e se houve alteração em alguma coluna para que
        seja atualizados
        :param dados_sis_crm_churn: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tb_churn_silver = self.tb_sis_crm_churn_silver()
        registros_atualizados_sis_crm_churn = []
        for item in dados_sis_crm_churn:
            try:
                for nm_coluna in tb_churn_silver.columns[1:len(tb_churn_silver.columns) - 1]:
                    dsc = tb_churn_silver.filter(
                        pl.col(tb_churn_silver.columns[0]) == str(item[tb_churn_silver.columns[0]])
                    )[nm_coluna].to_list()[0]
                    if dsc != item[nm_coluna]:
                        registros_atualizados_sis_crm_churn.append(item)
            except IndexError:
                continue

        return registros_atualizados_sis_crm_churn

    def rotina_atualizacao(self, ids_existentes: list, lista_dados_bronze: list):
        """
        Rotina de verificação de dados atualizados da camada bronze para a silver e atualiza os respectivos dados
        na tabela 'tb_sis_crm_churn' na camada Silver
        :param ids_existentes: [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, ...]
        :param lista_dados_bronze: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: None
        """
        lista_dados_bronze_existentes = self.filtrar_dados(
            lista_ids=ids_existentes,
            dados_camada_bronze=lista_dados_bronze
        )

        lista_dicionario_dados_existentes = self.tratar_colunas(list_dict_tabela=lista_dados_bronze_existentes)
        dados_atualizados = self.verifica_dados_atualizados(dados_sis_crm_churn=lista_dicionario_dados_existentes)
        if dados_atualizados:
            DBCrmChur().atualizar_tb_sis_crm_churn(lista_dicionario_dados=dados_atualizados)
            print(f'{len(dados_atualizados)} Dado(s) Atualizado(s)')
        else:
            print('Nenhum dado atualizado')

    def rotina_novos(self, ids_novos: list, lista_dados_bronze: list) -> None:
        """
        Rotina de inserção de novos dados na tabela de 'tb_sis_crm_churn' na camada Silver
        :param ids_novos: [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, ...]
        :param lista_dados_bronze: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: None
        """
        lista_dados_bronze_novos = self.filtrar_dados(
            lista_ids=ids_novos,
            dados_camada_bronze=lista_dados_bronze
        )
        if lista_dados_bronze_novos:
            lista_dicionario_dados_novos = self.tratar_colunas(list_dict_tabela=lista_dados_bronze_novos)
            DBCrmChur().inserir_tb_sis_crm_churn(lista_dicionario_dados=lista_dicionario_dados_novos)
            print(f'{len(lista_dados_bronze_novos)} Dado(s) Novo(s) Inserido(s)')
        else:
            print('Nenhum dado novo Inserido')

    def executar(self) -> None:
        """
        Rotina de ingestão da tabela 'tb_sis_crm_churn' na camada Silver
        :return: None
        """
        lista_dados_bronze = self.transformar_dataframe_dicionario()
        ids_novos, ids_existentes = self.comparar_ids_entre_camadas(
            ids_bronze=self.obter_ids_bronze(lista_dados_bronze),
            ids_silver=self.ids_sis_crm_churn_silver()
        )

        self.rotina_atualizacao(ids_existentes=ids_existentes, lista_dados_bronze=lista_dados_bronze)
        self.rotina_novos(ids_novos=ids_novos, lista_dados_bronze=lista_dados_bronze)

if __name__ == '__main__':
    SilverSisCrmChurn().executar()
