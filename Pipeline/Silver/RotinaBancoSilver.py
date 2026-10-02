from BancoDados.conexao import DBAuditoria
from pyodbc import connect
import polars as pl


class RotinaBanco:
    def __init__(self, nome_tabela: str):
        self.__conexao = connect(DBAuditoria().engine)
        self.__nm_tabela_banco = nome_tabela

    def tb_sis_crm_churn_bronze(self) -> pl.DataFrame:
        """
        Consulta o banco de dados e retorna toda a tabela de 'nome_tabela' como um pl.DataFrame
        :return: pl.DataFrame
        """
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(f"""select * from {self.__nm_tabela_banco}""")
            consulta_estado_civil = pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return consulta_estado_civil

    @property
    def conexao(self):
        return self.__conexao
