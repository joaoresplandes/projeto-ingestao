from datetime import datetime
from BancoDados.rotina_banco import RotinaBanco


class DBGold(RotinaBanco):
    def __init__(self):
        self.__nm_tb_churn_marketing: str = 'projeto_churn.gold.tb_churn_marketing'
        super().__init__()

    @staticmethod
    def lista_dados_novos(lista_dados: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem inseridas
        no banco de dados na tabela 'tb_churn_marketing'
        :param lista_dados: {'id': 1, 'cpf': 12345678901, 'idgenero': 'F', 'codestadocivil': 3, 'idade': 25, ... }
        :return: [('1', 12345678901, 'F', 3, 25, 'SE', 11, 0, 202405 ), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
                            idade,
                            uf,
                            ind_cliente,
                            ano_mes,
                            estado_civil,
                            escolaridade,
                            mensalidade,
                            participacao,
                            data_insercao
                        )
                        values ({placeholder})
                    """,
                    self.lista_dados_novos(lista_dados=lista_dicionario_dados)
                )
