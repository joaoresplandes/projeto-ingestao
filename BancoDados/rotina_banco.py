from BancoDados.conexao import DBAuditoria
from pyodbc import connect
import polars as pl


class RotinaBanco:
    def __init__(self):
        self.__conexao = connect(DBAuditoria().engine)

    def tabela(self, nm_tabela: str) -> pl.DataFrame:
        """
        Consulta o banco de dados e retorna toda a tabela de 'nm_tabela' como um pl.DataFrame
        :return: pl.DataFrame
        """
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(f"select * from {nm_tabela}")
            consulta_tb_crm_churm_silver= pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return consulta_tb_crm_churm_silver

    def ids(self, nm_tabela: str) -> list:
        """
        Retorna a lista de todos os ids da tabela 'nm_tabela'
        :return: [1, 2, 4, 5, 6, 7, ...]
        """
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(f"select * from {nm_tabela}")
            lista_ids= pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )['id'].to_list()

        return lista_ids

    @property
    def conexao(self):
        return self.__conexao
