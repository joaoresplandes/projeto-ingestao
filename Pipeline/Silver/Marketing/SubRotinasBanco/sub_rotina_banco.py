from BancoDados.rotina_banco import RotinaBanco
from datetime import datetime
from pyodbc import Error


class DBSilver(RotinaBanco):
    def __init__(self):
        self.__nm_tb_churn_marketing: str = 'projeto_churn.silver.tb_churn_marketing'
        super().__init__()

    @staticmethod
    def lista_dados_novos(lista_dados_churn: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem inseridas
        no banco de dados na tabela 'tb_churn_marketing'
        :param lista_dados_churn: {'id': 1, 'cpf': 12345678901, 'idgenero': 'F', 'codestadocivil': 3, 'idade': 25, ... }
        :return: [('1', 12345678901, 'F', 3, 25, 'SE', 11, 0, 202405 ), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados_churn:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            lista_tuplas_crm_churn.append(tuple(lista_dados_original))

        return lista_tuplas_crm_churn

    @staticmethod
    def lista_dados_atualizacao(lista_dados_churn: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem
        atualizados no banco de dados na tabela 'tb_churn_marketing', com o id na ultima posicao
        :param lista_dados_churn: {'id': 1, 'cpf': 12345678901, 'idgenero': 'F', 'codestadocivil': 3, 'idade': 25, ... }
        :return: [(12345678901, 'F', 3, 25, 'SE', 11, 0, 202405, '1'), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados_churn:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            lista_dados_original.append(lista_dados_original[0])
            del lista_dados_original[0]
            lista_tuplas_crm_churn.append(tuple(lista_dados_original))

        return lista_tuplas_crm_churn

    def inserir_dados_marketing(self, lista_dicionario_dados: list) -> None:
        """
        Insere os dados que contem em 'lista_dicionario_dados' no banco 'tb_churn_marketing' na camada silver
        :param lista_dicionario_dados: {'id': 1, 'cpf': 12345678901, 'idgenero': 'F', 'codestadocivil': 3, ... }
        :return: None
        """
        placeholder = ', '.join('?' for _ in lista_dicionario_dados[0].keys()) + ', ?'
        with self.conexao as conexao:
            with conexao.cursor() as cursor:
                cursor.fast_executemany = True
                cursor.executemany(
                    f"""
                        insert into {self.__nm_tb_churn_marketing}(
                            id,
                            genero,
                            codestadocivil,
                            idade,
                            uf,
                            codescolaridade,
                            indcliente,
                            ano_mes,
                            data_insercao
                        )
                        values ({placeholder})
                    """,
                    self.lista_dados_novos(lista_dados_churn=lista_dicionario_dados)
                )

    def atualizar_tb_marketing(self, lista_dicionario_dados: list) -> None:
        """
        Atualiza a tabela 'tb_churn_marketing' caso algum dado ja gravado tenha sido alterado na fonte
        :param lista_dicionario_dados: {'id': 1, 'cpf': 12345678901, 'idgenero': 'F', 'codestadocivil': 3, ... }
        :return: None
        """
        try:
            with self.conexao:
                with self.conexao.cursor() as cursor:
                    cursor.executemany(
                        f"""
                            update {self.__nm_tb_churn_marketing}
                            genero cpf = ?,
                            codestadocivil = ?,
                            idade = ?,
                            uf = ?,
                            codescolaridade = ?,
                            indcliente = ?,
                            ano_mes = ?,
                            data_insercao = ?
                        """,
                        self.lista_dados_atualizacao(lista_dados_churn=lista_dicionario_dados)
                    )
        except Error as e:
            print(f'Erro de atualização: {e}')
        finally:
            self.conexao.close()
