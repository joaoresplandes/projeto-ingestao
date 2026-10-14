from Pipeline.Gold.Marketing.DBMarketing.rotina_banco_marketing import DBGold
from BancoDados.rotina_banco import RotinaBanco
import polars as pl


class FluxoBanco(RotinaBanco):
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela
        self.__nm_marketing_gold: str = 'projeto_churn.gold.tb_churn_marketing'
        super().__init__()
        self.__tb_marketing_gold = self.tabela(nm_tabela=self.__nm_marketing_gold)


    def verificar_registros_novos(self) -> list:
        """
        Retorna uma lista dos ids que não contem ainda no banco de dados
        :return: [1, 2, 3, ...]
        """
        ids_novos = [
            num_id for num_id in [num_id for num_id in self.__tabela['id']]
            if num_id not in self.ids(nm_tabela=self.__nm_marketing_gold)
        ]

        return ids_novos

    def filtrar_tabela(self) -> pl.DataFrame:
        """
        Retorna um DataFrame filtrado pelos ids que ainda não constam no banco de dados
        :return: pl.DataFrame
        """
        tabela = self.__tabela.filter(pl.col('id').is_in(self.verificar_registros_novos()))

        return tabela

    @staticmethod
    def transformar_dataframe_dicionario(tabela: pl.DataFrame) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela_temp = tabela.with_columns(
            pl.Series([index for index in range(tabela.shape[0])]).alias('index')
        )
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela.columns[:]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados

    def executar(self) -> None:
        """
        Rotina de insercao de dados novos na tabela de marketing na cama gold do banco de dados
        :return: pl.DataFrame
        """
        lista_dicionarios_marketing = self.transformar_dataframe_dicionario(tabela=self.filtrar_tabela())
        if lista_dicionarios_marketing:
            DBGold().inserir_dados_marketing(lista_dicionario_dados=lista_dicionarios_marketing)
