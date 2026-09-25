from BancoDados.conexao import DBAuditoria
from pyodbc import connect
import polars as pl


class DBEstadoCivil:
    def __init__(self):
        self.__conexao = connect(DBAuditoria().engine)
        self.__nm_tb_estado_civil: str = 'projeto_churn.bronze.tb_estado_civil'


    def consultar_tb_estado_civil(self, tupla_ids: tuple) -> pl.DataFrame:
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(
                f"""
                select * from {self.__nm_tb_estado_civil}
                where id_ec in {tupla_ids}
                """
            )
            consulta_estado_civil = pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return consulta_estado_civil

    def consultar_tb_estado_civil_completo(self) -> pl.DataFrame:
        with self.__conexao.cursor() as cursor:
            consulta = cursor.execute(f"""select * from {self.__nm_tb_estado_civil}"""
            )
            consulta_estado_civil = pl.DataFrame(
                [tuple(row) for row in consulta.fetchall()],
                schema=[desc[0] for desc in cursor.description],
                orient='row'
            )

        return consulta_estado_civil

    def inserir_tb_estado_civil(self, dicionario_dados: dict) -> None:
        """
        Insere os dados de 'dicionario_dados' na tabela 'estado_civil'
        :param dicionario_dados: {
        'ID_EC': [1, 2, 3, 4, 5, 6],
        'DSC_EC': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável', 'Separado(a)']
        }
        :return: None
        """
        dados = [(int(id), dicionario_dados["DSC_EC"][index]) for index, id in enumerate(dicionario_dados['ID_EC'])]
        with self.__conexao.cursor() as cursor:
            for id, dsc in dados:
                cursor.execute(
                    f"""
                    insert into {self.__nm_tb_estado_civil}(id_ec, dsc_ec)
                    values ({id}, '{dsc}')
                    """
                )