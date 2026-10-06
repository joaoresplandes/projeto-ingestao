from BancoDados.conexao import DBAuditoria
from pyodbc import connect
import polars as pl


class CamadaBronze:
    def __init__(self):
        self.__conexao = connect(DBAuditoria().engine)
        self.__nm_tb_churn_bronze: str = r'projeto_churn.bronze.tb_sis_crm_churn'

    def tb_sis_crm_churn_bronze(self) -> pl.DataFrame:
        """
        Consulta o banco de dados e retorna toda a tabela de 'nome_tabela' como um pl.DataFrame
        :return: pl.DataFrame
        """
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(f"select * from {self.__nm_tb_churn_bronze}")
            consulta_sis_crm_bronze = pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return consulta_sis_crm_bronze

    def ids_sis_crm_churn_bronze(self) -> list:
        """
        Retorna a lista de todos os ids da base
        :return: [1, 2, 4, 5, 6, 7, ...]
        """
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(f"select * from {self.__nm_tb_churn_bronze}")
            lista_ids = pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )['id'].to_list()

        return lista_ids
