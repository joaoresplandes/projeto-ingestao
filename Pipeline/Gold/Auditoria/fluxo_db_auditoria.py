from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
from datetime import datetime


class DBAuditoria(RotinaBanco):
    def __init__(self):
        self.__tabela_auditoria_silver: str = 'projeto_churn.silver.tb_cliente_churn_auditoria'
        super().__init__()

    @staticmethod
    def lista_dados_auditoria(lista_dados_auditoria: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem inseridas
        no banco de dados na tabela 'tb_sis_crm_churn'
        :param lista_dados_auditoria: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ... }
        :return: [
            ('1', '123.456.789-01', 'Alice', 'Alves', 'Feminino',
            '3', '25', 'SE', '11', '0', '05', '2024', '2026-09-27 13:50:46'), ... ]
        """
        lista_tuplas_auditoria = []
        for dado in lista_dados_auditoria:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            lista_tuplas_auditoria.append(tuple(lista_dados_original))

        return lista_tuplas_auditoria

    def inserir_tb_auditoria(self, lista_dicionario_dados: list) -> None:
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
                    insert into {self.__tabela_auditoria_silver}(
                        id,
                        cpf,
                        nome_completo,
                        genero,
                        ind_cliente,
                        ano_mes,
                        data_insercao
                    )
                    values ({placeholder})
                """,
                self.lista_dados_auditoria(lista_dados_auditoria=lista_dicionario_dados)
            )
