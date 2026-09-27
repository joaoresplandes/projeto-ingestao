import pyodbc
import polars as pl
from BancoDados.conexao import DBAuditoria


class BancoDados:
    def __init__(self):
        self.__conexao = pyodbc.connect(DBAuditoria().engine)
        self.__NOME_TABELA_AUDITORIA: str = 'projeto_churn.silver.cliente_churn_auditoria'
        self.__NOME_TABELA_PERFIL_CLIENTE: str = 'projeto_churn.bronza.perfil_cliente'

    def consultar_tabela(self) -> pl.DataFrame:
        with self.__conexao.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.__NOME_TABELA_AUDITORIA}")
            tabela_consulta = pl.DataFrame(
                [tuple(row) for row in cursor.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return tabela_consulta

    def consulta_perfil_cliente(self, lista_ids: tuple) -> pl.DataFrame:
        """
        realiza uma consulta no banco de perfil cliente para os ids informados em 'lista_ids'
        :param lista_ids: (1, 5, 4, 15, 3)
        :return: pl.DataFrame
        """
        with self.__conexao.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    ID,
                    VLR_MENSAL,
                    VLR_COPARTICIPACAO
                FROM {self.__NOME_TABELA_PERFIL_CLIENTE}
                WHERE ID IN {lista_ids}"""
            )
            consulta_perfil = pl.DataFrame(
                [tuple(row) for row in cursor.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return consulta_perfil


    def inserir_dados(self, tabela_dados: pl.DataFrame) -> None:
        """
        Realiza a inserção dos dados novos na tabela
        :param tabela_dados:
        :return:
        """
        placeholders = ", ".join("?" for _ in tabela_dados.columns)
        with self.__conexao.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {self.__NOME_TABELA_AUDITORIA}')
            cursor.fast_executemany = True
            cursor.executemany(
                f"""
                    INSERT INTO {self.__NOME_TABELA_AUDITORIA}(
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
