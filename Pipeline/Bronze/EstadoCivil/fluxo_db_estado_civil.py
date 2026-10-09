from BancoDados.rotina_banco import RotinaBanco
from datetime import datetime
import polars as pl


class DBEstadoCivil(RotinaBanco):
    def __init__(self):
        self.__nm_tb_estado_civil: str = 'projeto_churn.bronze.tb_estado_civil'
        super().__init__()


    def consultar_tb_estado_civil(self, tupla_ids: tuple) -> pl.DataFrame:
        """
        Consulta o banco de dados e retorna uma tabela filtrada de acordo com os IDS informados em 'tupla_ids',
        resultando em um pl.DataFrame
        :param tupla_ids: (1, 2, 4, 5, 7)
        :return: pl.DataFrame
        """
        with self.conexao.cursor() as cursor:
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

    def inserir_tb_estado_civil(self, dicionario_dados: dict) -> None:
        """
        Insere os dados de 'dicionario_dados' na tabela 'estado_civil'
        :param dicionario_dados: {
        'ID_EC': [1, 2, 3, 4, 5, 6],
        'DSC_EC': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável', 'Separado(a)']
        }
        :return: None
        """
        dados = [(int(nm_id), dicionario_dados["DSC_EC"][index]) for index, nm_id in enumerate(dicionario_dados['ID_EC'])]
        with self.conexao.cursor() as cursor:
            for nm_id, dsc in dados:
                cursor.execute(
                    f"""
                    insert into {self.__nm_tb_estado_civil}(id_ec, dsc_ec, dt_atualizacao)
                    values ({nm_id}, '{dsc}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')
                    """
                )

    def atualizar_tb_estado_civil(self, dicionario_dados: dict) -> None:
        """
        Atualiza os dados informados no 'dicionaros_dados'
        :param dicionario_dados: {
        'ID_EC': [1, 2, 3, 4, 5, 6],
        'DSC_EC': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável', 'Separado(a)']
        }
        :return: None
        """
        dados = [(int(nm_id), dicionario_dados["DSC_EC"][index]) for index, nm_id in enumerate(dicionario_dados['ID_EC'])]
        with self.conexao.cursor() as cursor:
            for nm_id, dsc in dados:
                cursor.execute(
                    f"""
                    update {self.__nm_tb_estado_civil}
                    set dsc_ec = '{dsc}', dt_atualizacao = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'
                    where id_ec = {nm_id}
                    """
                )
