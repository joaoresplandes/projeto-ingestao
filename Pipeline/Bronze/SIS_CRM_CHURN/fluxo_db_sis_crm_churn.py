from Pipeline.Bronze.RotinasBanco import RotinaBanco
from datetime import datetime
import polars as pl


class DBSisChurn(RotinaBanco):
    def __init__(self):
        self.__nm_tb_sis_crm_churn: str = 'projeto_churn.bronze.tb_sis_crm_churn'
        super().__init__(nome_tabela=self.__nm_tb_sis_crm_churn)


    @staticmethod
    def lista_dados_sis_crm_churn(lista_dados_churn: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem inseridas
        no banco de dados na tabela 'tb_sis_crm_churn'
        :param lista_dados_churn: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ... }
        :return: [
            ('1', '123.456.789-01', 'Alice', 'Alves', 'Feminino',
            '3', '25', 'SE', '11', '0', '05', '2024', '2026-09-27 13:50:46'), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados_churn:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            lista_tuplas_crm_churn.append(tuple(lista_dados_original))

        return lista_tuplas_crm_churn

    @staticmethod
    def lista_dados_sis_crm_churn_atualizacao(lista_dados_churn: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem
        atualizados no banco de dados na tabela 'tb_sis_crm_churn', com o id na ultima posicao
        :param lista_dados_churn: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ... }
        :return: [
            ('123.456.789-01', 'Alice', 'Alves', 'Feminino',
            '3', '25', 'SE', '11', '0', '05', '2024', '2026-09-27 13:50:46', '1'), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados_churn:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            lista_dados_original.append(lista_dados_original[0])
            del lista_dados_original[0]
            lista_tuplas_crm_churn.append(tuple(lista_dados_original))

        return lista_tuplas_crm_churn


    def inserir_tb_sis_crm_churn(self, lista_dicionario_dados: list) -> None:
        """
        Insere os dados brutos na tabela de 'tb_sis_crm_churn'
        :param lista_dicionario_dados: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ... }
        :return: None
        """
        placeholder = ', '.join('?' for _ in lista_dicionario_dados[0].keys()) + ', ?'
        with self.conexao.cursor() as cursor:
            cursor.fast_executemany = True
            cursor.executemany(
                f"""
                    insert into {self.__nm_tb_sis_crm_churn}(
                        id,
                        cpf,
                        nome,
                        sobrenome,
                        idgenero,
                        estado_civil,
                        idade,
                        uf,
                        escolaridade,
                        indcliente,
                        mes,
                        ano,
                        dt_atualizacao
                    )
                    values ({placeholder})
                """,
                self.lista_dados_sis_crm_churn(lista_dados_churn=lista_dicionario_dados)

            )
    def atualizar_tb_sis_crm_churn(self, lista_dicionario_dados: list) -> None:
        pass

