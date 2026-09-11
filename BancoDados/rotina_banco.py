import pyodbc
import polars as pl
from BancoDados.conexao import DBAuditoria


class BancoDados:
    def __init__(self):
        self.__conexao = pyodbc.connect(DBAuditoria().ENGINE)
        self.__NOME_TABELA: str = 'PROJETO_CHURN_AUDITORIA.dbo.CLIENTE_CHURN_AUDITA'

    def consultar_tabela(self) -> pl.DataFrame:
        with self.__conexao.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.__NOME_TABELA}")
            tabela_consulta = pl.DataFrame(
                [tuple(row) for row in cursor.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return tabela_consulta

    def

    def inserir_dados(self, tabela_dados: pl.DataFrame) -> None:
        placeholders = ", ".join("?" for _ in tabela_dados.columns)

        with self.__conexao.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {self.__NOME_TABELA}')
            cursor.fast_executemany = True
            cursor.executemany(
                f"""
                    INSERT INTO {self.__NOME_TABELA}(
                    ID_CLI, 
                    CPF_CLI, 
                    NOME_COMPLETO_CLI,
                    GENERO, 
                    IND_CLIENTE, 
                    ANO_MES, 
                    DATA_INSERCAO
                )
                VALUES ({placeholders})
                """,
                [tuple(row) for row in tabela_dados.iter_rows()]
            )
