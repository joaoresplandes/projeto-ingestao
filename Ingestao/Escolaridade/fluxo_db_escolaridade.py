from Ingestao.RotinasBanco import RotinaBanco
from datetime import datetime


class DBEscolaridade(RotinaBanco):
    def __init__(self):
        self.__nm_tb_escolaridade: str = 'projeto_churn.bronze.tb_escolaridade'
        super().__init__(nome_tabela=self.__nm_tb_escolaridade)

    def atualizar_tb_escolaridade(self, dicionario_dados: dict) -> None:
        """
        Atualiza os dados informados no 'dicionaros_dados'
        :param dicionario_dados: {
            'ID_ESCOLARIDADE': ['1', '2', ...],
            'DESC_ESCOLARIDADE': ['Ensino Fundamental Incompleto', ...]
        }
        :return: None
        """
        dados = [
            (int(nm_id), dicionario_dados["DESC_ESCOLARIDADE"][index])
            for index, nm_id in enumerate(dicionario_dados['ID_ESCOLARIDADE'])
        ]
        with self.conexao.cursor() as cursor:
            for nm_id, dsc in dados:
                cursor.execute(
                    f"""
                    update {self.__nm_tb_escolaridade}
                    set desc_escolaridade = '{dsc}', dt_atualizacao = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'
                    where id_escolaridade = {nm_id}
                    """
                )

    def inserir_tb_escolaridade(self, dicionario_dados: dict) -> None:
        """
        Insere os dados de 'dicionario_dados' na tabela 'escolaridade'
        :param dicionario_dados: {
            'ID_ESCOLARIDADE': ['1', '2', ...],
            'DESC_ESCOLARIDADE': ['Ensino Fundamental Incompleto', ...]
        }
        :return: None
        """
        dados = [
            (int(nm_id), dicionario_dados["DESC_ESCOLARIDADE"][index])
            for index, nm_id in enumerate(dicionario_dados['ID_ESCOLARIDADE'])
        ]
        with self.conexao.cursor() as cursor:
            for nm_id, dsc in dados:
                cursor.execute(
                    f"""
                    insert into {self.__nm_tb_escolaridade}(id_escolaridade, desc_escolaridade, dt_atualizacao)
                    values ({nm_id}, '{dsc}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')
                    """
                )
