from datetime import datetime
from BancoDados.rotina_banco import RotinaBanco


class DBGold(RotinaBanco):
    def __init__(self):
        self.__nm_tb_churn_analitico: str = 'projeto_churn.gold.tb_churn_analitico'
        super().__init__()

    @staticmethod
    def lista_dados_novos(lista_dados: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem inseridas
        no banco de dados na tabela 'tb_churn_analitico'
        :param lista_dados: {'genero': 'F', 'uf': 'MA', 'ano_mes': 202405, 'estado_civil': 'União Estável', ... }
        :return: [('F', 'MA', 202405, 'União Estável', 'Ensino Médio Incompleto', 'Jovem', 1, 675, 0}), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            lista_tuplas_crm_churn.append(tuple(lista_dados_original))

        return lista_tuplas_crm_churn


    def inserir_dados_analiticos(self, lista_dicionario_dados: list) -> None:
        """
        Insere os dados que contem em 'lista_dicionario_dados' no banco 'tb_churn_analitico' na camada silver
        :param lista_dicionario_dados: {'genero': 'F', 'uf': 'MA', 'ano_mes': 202405, ... }
        :return: None
        """
        placeholder = ', '.join('?' for _ in lista_dicionario_dados[0].keys()) + ', ?'
        with self.conexao as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(f'Truncate table {self.__nm_tb_churn_analitico}')
                cursor.fast_executemany = True
                cursor.executemany(
                    f"""
                        insert into {self.__nm_tb_churn_analitico}(
                            genero,
                            uf,
                            ano_mes,
                            estado_civil,
                            escolaridade,
                            faixa_etaria,
                            total_churn,
                            valor_mensalidade_mes,
                            valor_participacao_mes,
                            data_insercao
                        )
                        values ({placeholder})
                    """,
                    self.lista_dados_novos(lista_dados=lista_dicionario_dados)
                )
