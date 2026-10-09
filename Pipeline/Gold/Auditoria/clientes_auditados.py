from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Gold.Auditoria.SubRotinas.sub_rotinas import TratarAuditoria
from Pipeline.Gold.Auditoria.fluxo_db_auditoria import DBGold
import polars as pl


class Auditoria(RotinaBanco):
    def __init__(self):
        self.__nm_tabela_sis_crm_churn_sem_duplicatas = 'projeto_churn.silver.tb_sis_crm_churn_sem_duplicatas'
        self.__nm_tabela_auditoria_gold: str = 'projeto_churn.gold.tb_cliente_churn_auditoria'
        super().__init__()
        self.__tb_sis_crm_churn_sem_duplicatas = self.tabela(nm_tabela=self.__nm_tabela_sis_crm_churn_sem_duplicatas)
        self.__tb_sis_crm_churn_sem_duplicatas = self.filtrar_clientes_auditados()

    def filtrar_clientes_auditados(self) -> pl.DataFrame:
        """
        Filtra a tabela 'tb_sis_crm_churn' com o 'indcliente' igual a 1 como solicitado pela equipe de auditoria
        :return: tabela filtrada com indcliente == 1
        """
        return self.__tb_sis_crm_churn_sem_duplicatas.filter(pl.col('indcliente') == 1)

    @staticmethod
    def transformar_dataframe_dicionario(tabela_churn_silva: pl.DataFrame) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela_temp = tabela_churn_silva.with_columns(
            pl.Series([index for index in range(tabela_churn_silva.shape[0])]).alias('index')
        )
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela_churn_silva.columns[:]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados


    @staticmethod
    def verificar_dados_novos(dados_entrada: list, dados_auditoria_gold: list):
        """
        Retorna uma lista de dicionarios dos dados que ainda não contem na tabela 'tb_cliente_churn_auditoria' na
        camada gold
        :param dados_entrada: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        :param dados_auditoria_gold: [{'id': 3, 'cpf': 34567800223, 'nome_completo': 'Aline Abreu', ...}]
        :return: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        """
        ids_auditoria_gold = [dicionario['id'] for dicionario in dados_auditoria_gold]
        dados_novos = [dado for dado in [dado for dado in dados_entrada] if dado['id'] not in ids_auditoria_gold]

        return dados_novos

    def varredura_dados_atualizados(self, dados_auditoria: list) -> list:
        """
        Verifica se os dados de 'dados_sis_crm_churn' contem no banco e se houve alteração em alguma coluna para que
        seja atualizados
        :param dados_auditoria: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tb_churn_silver = self.tabela(nm_tabela=self.__nm_tabela_sis_crm_churn_sem_duplicatas)
        registros_atualizados_sis_crm_churn = []
        for item in dados_auditoria:
            try:
                for nm_coluna in tb_churn_silver.columns[1:len(tb_churn_silver.columns) - 1]:
                    dsc = tb_churn_silver.filter(
                        pl.col(tb_churn_silver.columns[0]) == str(item[tb_churn_silver.columns[0]])
                    )[nm_coluna].to_list()[0]
                    if dsc != item[nm_coluna]:
                        registros_atualizados_sis_crm_churn.append(item)
            except IndexError:
                continue

        return registros_atualizados_sis_crm_churn

    def verificar_dados_atualizados(self, dados_entrada: list, dados_auditoria_gold: list):
        """
        Retorna uma lista de dicionarios dos dados que ainda não contem na tabela 'tb_cliente_churn_auditoria' na
        camada gold para caso tenham alguma modificação, sejam atualizados
        :param dados_entrada: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        :param dados_auditoria_gold: [{'id': 3, 'cpf': 34567800223, 'nome_completo': 'Aline Abreu', ...}]
        :return: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        """
        ids_auditoria_gold = [dicionario['id'] for dicionario in dados_auditoria_gold]
        dados_existentes = [dado for dado in [dado for dado in dados_entrada] if dado['id'] in ids_auditoria_gold]

        return self.varredura_dados_atualizados(dados_auditoria=dados_existentes)


    def rotina_dados_novos(self) -> None:
        """
        Rotina de inserção de novos dados na tabela de auditoria na cama gold
        :return: None
        """
        tabela_auditoria = TratarAuditoria.executar_tratativa_auditoria(
            tb_auditoria=self.__tb_sis_crm_churn_sem_duplicatas
        )
        dicionario_dados_auditoria = self.transformar_dataframe_dicionario(tabela_churn_silva=tabela_auditoria)
        tb_auditoria_gold = self.tabela(nm_tabela=self.__nm_tabela_auditoria_gold)
        dicionario_auditoria_gold = self.transformar_dataframe_dicionario(tabela_churn_silva=tb_auditoria_gold)

        novos_dados = self.verificar_dados_novos(
            dados_entrada=dicionario_dados_auditoria,
            dados_auditoria_gold=dicionario_auditoria_gold
        )
        if novos_dados:
            DBGold().inserir_tb_auditoria(lista_dicionario_dados=novos_dados)
            print(f'{len(novos_dados)} dado(s) atualizado(s) na tabela "{self.__nm_tabela_auditoria_gold}"')

    def rotina_dados_atualizados(self) -> None:
        """
        Rotina de atualizacao dos dados de auditoria na cama gold
        :return: None
        """
        tabela_auditoria = TratarAuditoria.executar_tratativa_auditoria(
            tb_auditoria=self.__tb_sis_crm_churn_sem_duplicatas
        )
        dicionario_dados_auditoria = self.transformar_dataframe_dicionario(tabela_churn_silva=tabela_auditoria)
        tb_auditoria_gold = self.tabela(nm_tabela=self.__nm_tabela_auditoria_gold)
        dicionario_auditoria_gold = self.transformar_dataframe_dicionario(tabela_churn_silva=tb_auditoria_gold)

        novos_atualizado = self.verificar_dados_atualizados(
            dados_entrada=dicionario_dados_auditoria,
            dados_auditoria_gold=dicionario_auditoria_gold
        )
        if novos_atualizado:
            DBGold().atualizar_tb_auditoria(lista_dicionario_dados=novos_atualizado)
            print(f'{len(novos_atualizado)} dado(s) atualizado(s) na tabela "{self.__nm_tabela_auditoria_gold}"')

    def rotina_auditoria(self) -> None:
        """
        Rotina principal de auditoria na cama gold
        :return: None
        """
        self.rotina_dados_atualizados()
        self.rotina_dados_novos()
