from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Silver.Marketing.SubRotina.sub_rotinas import SubRotinas
from Pipeline.Silver.Marketing.SubRotinasBanco.sub_rotina_banco import DBSilver
import polars as pl


class Marketing(RotinaBanco):
    def __init__(self):
        self.__nm_tabela_sis_crm_churn_sem_duplicatas = 'projeto_churn.silver.tb_sis_crm_churn_sem_duplicatas'
        self.__nm_tabela_marketin_silver: str = 'projeto_churn.silver.tb_churn_marketing'
        super().__init__()
        self.__tb_sis_crm_churn_sem_duplicatas = self.tabela(nm_tabela=self.__nm_tabela_sis_crm_churn_sem_duplicatas)
        self.__tb_sis_crm_churn_sem_duplicatas = self.filtrar_colaboradores_validos()

    def filtrar_colaboradores_validos(self) -> pl.DataFrame:
        """
        Obtem a tabela sem dados duplicados e filtra apenas os colaboradores ativos -> indcliente == 1
        :return: tabela filtrada com indcliente != 1
        """
        tabela_mkt = self.tabela(self.__nm_tabela_sis_crm_churn_sem_duplicatas).filter(pl.col('indcliente') != 1)

        return tabela_mkt

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
    def verificar_dados_novos(dados_entrada: list, dados_marketing_silver: list):
        """
        Retorna uma lista de dicionarios dos dados que ainda não contem na tabela 'tb_cliente_churn_auditoria' na
        camada gold
        :param dados_entrada: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        :param dados_marketing_silver: [{'id': 3, 'cpf': 34567800223, 'nome_completo': 'Aline Abreu', ...}]
        :return: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        """
        ids_auditoria_gold = [dicionario['id'] for dicionario in dados_marketing_silver]
        dados_novos = [dado for dado in [dado for dado in dados_entrada] if dado['id'] not in ids_auditoria_gold]

        return dados_novos

    def varredura_dados_atualizados(self, dados_marketing: list) -> list:
        """
        Verifica se os dados de 'dados_sis_crm_churn' contem no banco e se houve alteração em alguma coluna para que
        seja atualizados
        :param dados_marketing: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tb_churn_silver = self.tabela(nm_tabela=self.__nm_tabela_sis_crm_churn_sem_duplicatas)
        registros_atualizados_sis_crm_churn = []
        for item in dados_marketing:
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

    def verificar_dados_atualizados(self, dados_entrada: list, dados_marketing_silver: list):
        """
        Retorna uma lista de dicionarios dos dados que ainda não contem na tabela 'tb_cliente_churn_auditoria' na
        camada gold para caso tenham alguma modificação, sejam atualizados
        :param dados_entrada: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        :param dados_marketing_silver: [{'id': 3, 'cpf': 34567800223, 'nome_completo': 'Aline Abreu', ...}]
        :return: [{'id': 2, 'cpf': 23456700112, 'nome_completo': 'Ana Amaral', 'idgenero': 'F', ...}]
        """
        ids_auditoria_gold = [dicionario['id'] for dicionario in dados_marketing_silver]
        dados_existentes = [dado for dado in [dado for dado in dados_entrada] if dado['id'] in ids_auditoria_gold]

        return self.varredura_dados_atualizados(dados_marketing=dados_existentes)


    def rotina_dados_novos(self) -> None:
        """
        Rotina de inserção de dados novos na tabela 'tb_churn_marketing' na camada Silver
        :return: None
        """
        tabela_marketing = SubRotinas().executar(tabela_mkt=self.__tb_sis_crm_churn_sem_duplicatas)
        tb_marketing_silver = self.tabela(nm_tabela=self.__nm_tabela_marketin_silver)
        dados_novos = self.verificar_dados_novos(
            dados_entrada=self.transformar_dataframe_dicionario(tabela_churn_silva=tabela_marketing),
            dados_marketing_silver= self.transformar_dataframe_dicionario(tabela_churn_silva=tb_marketing_silver)
        )
        if dados_novos:
            DBSilver().inserir_dados_marketing(lista_dicionario_dados=dados_novos)
            print(f'{len(dados_novos)} dado(s) inseridos(s) na tabela "{self.__nm_tabela_marketin_silver}".')

    def rotina_dados_atualizados(self) -> None:
        """
        Rotina de atualizacao de dados novos na tabela 'tb_churn_marketing' na camada Silver
        :return: None
        """
        tabela_marketing = SubRotinas().executar(tabela_mkt=self.__tb_sis_crm_churn_sem_duplicatas)
        tb_marketing_silver = self.tabela(nm_tabela=self.__nm_tabela_marketin_silver)
        dados_atualizados = self.verificar_dados_atualizados(
            dados_entrada=self.transformar_dataframe_dicionario(tabela_churn_silva=tabela_marketing),
            dados_marketing_silver= self.transformar_dataframe_dicionario(tabela_churn_silva=tb_marketing_silver)
        )
        if dados_atualizados:
            DBSilver().atualizar_tb_marketing(lista_dicionario_dados=dados_atualizados)
            print(f'{len(dados_atualizados)} dado(s) inseridos(s) na tabela "{self.__nm_tabela_marketin_silver}".')

    @staticmethod
    def rotina() -> None:
        """
        Rotina de etl da tabela 'tb_churn_marketing' na camada Silver
        :return: None
        """
        Marketing().rotina_dados_atualizados()
        Marketing().rotina_dados_novos()
