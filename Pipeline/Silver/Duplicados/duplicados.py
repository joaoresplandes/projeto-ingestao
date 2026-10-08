from Pipeline.Silver.Duplicados.ValoresDuplicados.valores_duplicados import ValoresDuplicados
from Pipeline.Silver.Duplicados.ValoresNaoDuplicados.valores_sem_duplicados import ValoresNaoDuplicados
from Pipeline.Silver.Duplicados.SubRotinas.sub_rotinas import SubRotinaDuplicados
from Pipeline.Silver.Duplicados.SubRotinaBanco.sub_rotina_banco import SubRotinaBanco
from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
import polars as pl


class RotinaDuplicados(RotinaBanco):
    def __init__(self):
        self.__nm_tb_sis_crm_churn_silver: str = 'projeto_churn.silver.tb_sis_crm_churn'
        super().__init__()
        self._tabela = self.tb_camada_silver(nm_tabela=self.__nm_tb_sis_crm_churn_silver)
        self._lista_ids_duplicados = SubRotinaDuplicados.executar(tabela=self._tabela)

    def tabela_sem_duplicados(self) -> pl.DataFrame:
        """
        Executa a rotina de obter a tabela sem os cpfs duplicados
        :return: tabela filtrada sem os ultimos cpfs duplicados
        """
        tabela_sem_duplicados = ValoresNaoDuplicados.filtrar_tabela_sem_duplicados(
            tabela=self._tabela,
            id_duplicatos=self._lista_ids_duplicados
        )

        return tabela_sem_duplicados

    def tabela_com_duplicados(self) -> pl.DataFrame:
        """
        Retorna um dataframe com os ultimos registros inseridos de cpfs duplicados
        :return: tabela com os ultimos cpfs duplicados
        """
        tabela_com_duplicados = ValoresDuplicados.filtrar_tabela_duplicados(
            tabela=self._tabela,
            id_duplicatos=self._lista_ids_duplicados
        )

        return tabela_com_duplicados

    @staticmethod
    def transformar_dataframe_dicionario(tabela: pl.DataFrame) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela_temp = tabela.with_columns(pl.Series([index for index in range(tabela.shape[0])]).alias('index'))
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela.columns[:-1]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados

    def verificar_tb_duplicados(self, novos_dados: list, nm_tabela_banco: str) -> list:
        """
        Realiza uma verificação dos ids que ja estão gravados no banco para que não haja um reprocessamento e seja
        inserido apenas os dados novos no banco
        :param novos_dados: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ... }]
        :param nm_tabela_banco: 'projeto_churn.silver.tb_sis_crm_churn_sem_duplicatas'
        :return: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ... ]
        """
        lista_ids_banco = self.ids_camada_silver(nm_tabela=nm_tabela_banco)
        ids_novos = [
            num_id for num_id in [int(dicionario['id']) for dicionario in novos_dados]
            if num_id not in lista_ids_banco
        ]

        return ids_novos

    @staticmethod
    def verifica_dados_atualizados(dados_dicionario: list, tb_duplicados: pl.DataFrame) -> list:
        """
        Verifica se os dados de 'dados_dicionario' contem no banco e se houve alteração em alguma coluna para que
        seja atualizados
        :param tb_duplicados:
        :param dados_dicionario: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        registros_atualizados_sis_crm_churn = []
        for item in dados_dicionario:
            try:
                for nm_coluna in tb_duplicados.columns[1:len(tb_duplicados.columns) - 1]:
                    dsc = tb_duplicados.filter(pl.col(tb_duplicados.columns[0]) == int(item[tb_duplicados.columns[0]]))[nm_coluna].to_list()[0]
                    if dsc != item[nm_coluna]:
                        registros_atualizados_sis_crm_churn.append(item)
            except IndexError:
                continue

        return registros_atualizados_sis_crm_churn

    @staticmethod
    def selecionar_dados_para_insercao(lista_dicionario_dados: list, lista_ids: list) -> list:
        """
        Filtra apenas os ids que ainda não existem no banco informado por 'lista_ids' e insere o dicionario completo
        na nova lista 'lista_insercao'
        :param lista_dicionario_dados: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :param lista_ids: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ... ]
        :return: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        lista_insercao = [
            dicionario for dicionario in lista_dicionario_dados if dicionario['id'] in lista_ids
        ]

        return lista_insercao

    def rotina_inserir_dados_nao_duplicados(self) -> None:
        """
        Rotina de inserção dos novos dados sem duplicata na tabela "tb_sis_crm_churn_sem_duplicatas" da camada silver
        :return: None
        """
        dados_sem_duplicata = self.transformar_dataframe_dicionario(tabela=self.tabela_sem_duplicados())
        ids_novos_dados = self.verificar_tb_duplicados(
            novos_dados=dados_sem_duplicata,
            nm_tabela_banco='projeto_churn.silver.tb_sis_crm_churn_sem_duplicatas'
        )
        inserir_dados_sem_duplicata = self.selecionar_dados_para_insercao(
            lista_dicionario_dados=dados_sem_duplicata,
            lista_ids=ids_novos_dados
        )
        if inserir_dados_sem_duplicata:
            SubRotinaBanco().inserir_dados_nao_duplicados(lista_dicionario_dados=inserir_dados_sem_duplicata)
            print(f'{len(inserir_dados_sem_duplicata)} dado(s) inserido(s) na tabela "tb_sis_crm_churn_sem_duplicatas".')

    def rotina_inserir_dados_duplicados(self) -> None:
        """
        Rotina de inserção dos novos dados duplicados na tabela "tb_churn_cpfs_duplicados" da camada silver
        :return: None
        """
        dados_duplicatos = self.transformar_dataframe_dicionario(tabela=self.tabela_com_duplicados())

        ids_novos_dados_duplicatos = self.verificar_tb_duplicados(
            novos_dados=dados_duplicatos,
            nm_tabela_banco='projeto_churn.silver.tb_churn_cpfs_duplicados'
        )
        inserir_dados_duplicata = self.selecionar_dados_para_insercao(
            lista_dicionario_dados=dados_duplicatos,
            lista_ids=ids_novos_dados_duplicatos
        )

        if inserir_dados_duplicata:
            SubRotinaBanco().inserir_dados_duplicados(lista_dicionario_dados=dados_duplicatos)
            print(f'{len(inserir_dados_duplicata)} dado(s) inserido(s) na tabela "tb_churn_cpfs_duplicados".')

    def rotina_atualizar_dados_nao_duplicados(self) -> None:
        """
        Rotina de inserção dos novos dados sem duplicata na tabela "tb_sis_crm_churn_sem_duplicatas" da camada silver
        :return: None
        """
        dados_nao_duplicatos = self.transformar_dataframe_dicionario(tabela=self.tabela_sem_duplicados())
        tabela_nao_duplicados = self.tb_camada_silver(nm_tabela='projeto_churn.silver.tb_sis_crm_churn_sem_duplicatas')
        dados_a_ser_atualizados = self.verifica_dados_atualizados(
            dados_dicionario=dados_nao_duplicatos,
            tb_duplicados=tabela_nao_duplicados
        )
        if dados_a_ser_atualizados:
            SubRotinaBanco().atualizar_tb_nao_duplicados(lista_dicionario_dados=dados_a_ser_atualizados)
            print(f'{len(dados_a_ser_atualizados)} dado(s) atualizado(s) na tabela "tb_sis_crm_churn_sem_duplicatas".')

    def rotina_atualizar_dados_duplicados(self) -> None:
        """
        Rotina de inserção dos novos dados duplicados na tabela "tb_churn_cpfs_duplicados" da camada silver
        :return:
        """
        dados_nao_duplicatos = self.transformar_dataframe_dicionario(tabela=self.tabela_com_duplicados())
        tabela_nao_duplicados = self.tb_camada_silver(nm_tabela='projeto_churn.silver.tb_churn_cpfs_duplicados')
        dados_a_ser_atualizados = self.verifica_dados_atualizados(
            dados_dicionario=dados_nao_duplicatos,
            tb_duplicados=tabela_nao_duplicados
        )
        if dados_a_ser_atualizados:
            SubRotinaBanco().atualizar_tb_duplicados(lista_dicionario_dados=dados_a_ser_atualizados)
            print(f'{len(dados_a_ser_atualizados)} dado(s) atualizado(s) na tabela "tb_churn_cpfs_duplicados".')

    def rotina_dados_novos(self):
        self.rotina_inserir_dados_nao_duplicados()
        self.rotina_inserir_dados_duplicados()

    def rotina_dados_atualizados(self):
        self.rotina_atualizar_dados_nao_duplicados()
        self.rotina_atualizar_dados_nao_duplicados()


    def rotina_principal(self):
        self.rotina_dados_atualizados()
        self.rotina_dados_novos()

if __name__ == '__main__':
    RotinaDuplicados().rotina_principal()

