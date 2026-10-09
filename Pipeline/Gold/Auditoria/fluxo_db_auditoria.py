from BancoDados.rotina_banco import RotinaBanco
from pyodbc import Error


class DBGold(RotinaBanco):
    def __init__(self):
        self.__tabela_auditoria_gold: str = 'projeto_churn.gold.tb_cliente_churn_auditoria'
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
            lista_tuplas_auditoria.append(tuple(lista_dados_original))

        return lista_tuplas_auditoria

    @staticmethod
    def lista_dados_auditoria_atualizacao(lista_dados_churn: list) -> list:
        """
        Realiza o processo de obter os dados do dicionario e colocar dentro de uma lista de tuplas para serem
        atualizados no banco de dados na tabela 'tb_cliente_churn_auditoria', com o id na ultima posicao
        :param lista_dados_churn: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ... }
        :return: [
            ('123.456.789-01', 'Alice', 'Alves', 'Feminino',
            '3', '25', 'SE', '11', '0', '05', '2024', '2026-09-27 13:50:46', '1'), ... ]
        """
        lista_tuplas_crm_churn = []
        for dado in lista_dados_churn:
            lista_dados_original = list(dado.values())
            lista_dados_original.append(lista_dados_original[0])
            del lista_dados_original[0]
            lista_tuplas_crm_churn.append(tuple(lista_dados_original))

        return lista_tuplas_crm_churn

    def inserir_tb_auditoria(self, lista_dicionario_dados: list) -> None:
        """
        Insere os dados brutos na tabela de 'tb_sis_crm_churn'
        :param lista_dicionario_dados: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ... }
        :return: None
        """
        placeholder = ', '.join('?' for _ in lista_dicionario_dados[0].keys())
        with self.conexao.cursor() as cursor:
            cursor.fast_executemany = True
            cursor.executemany(
                f"""
                    insert into {self.__tabela_auditoria_gold}(
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

    def atualizar_tb_auditoria(self, lista_dicionario_dados: list) -> None:
        """
        Atualiza a tabela 'tb_cliente_churn_auditoria' caso algum dado ja gravado tenha sido alterado na fonte
        :param lista_dicionario_dados: {'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}
        :return: None
        """
        try:
            with self.conexao:
                with self.conexao.cursor() as cursor:
                    cursor.executemany(
                        f"""
                            update {self.__tabela_auditoria_gold}
                            set cpf = ?,
                                nome_completo = ?,
                                genero = ?,
                                ind_cliente = ?,
                                ano_mes = ?,
                                data_insercao = ?
                        """,
                        self.lista_dados_auditoria_atualizacao(lista_dados_churn=lista_dicionario_dados)
                    )
        except Error as e:
            print(f'Erro de atualização: {e}')
        finally:
            self.conexao.close()
