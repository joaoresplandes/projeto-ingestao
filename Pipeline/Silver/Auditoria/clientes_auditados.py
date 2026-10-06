from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
from Pipeline.Silver.Auditoria.SubRotinas.sub_rotinas import TratarAuditoria
from Pipeline.Silver.Auditoria.fluxo_db_auditoria import DBAuditoria
import polars as pl


class Auditoria(RotinaBanco):
    def __init__(self):
        self._nm_tabela_sis_crm_churn = 'projeto_churn.silver.tb_sis_crm_churn'
        super().__init__(nome_tabela=self._nm_tabela_sis_crm_churn)
        self.__tabela_sis_crm_churn = self.tb_sis_crm_churn_silver()
        self.__tabela_sis_crm_churn = self.filtrar_clientes_auditados()

    def filtrar_clientes_auditados(self) -> pl.DataFrame:
        """
        Filtra a tabela 'tb_sis_crm_churn' com o 'indcliente' igual a 1 como solicitado pela equipe de auditoria
        :return: tabela filtrada com indcliente == 1
        """
        return self.__tabela_sis_crm_churn.filter(pl.col('indcliente') == 1)

    def transformar_dataframe_dicionario(self, tabela_churn_silva: pl.DataFrame) -> list:
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
                for coluna in tabela_churn_silva.columns[:-1]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados

    def rotina_clientes_auditoria(self) -> None:
        """
        Filta a tabela pela coluna IndCliente, o que determina os clientes a serem analisados pelo time de auditoria
        :return: None
        """
        tabela_auditoria = TratarAuditoria.executar_tratativa_auditoria(tabela_auditoria=self.__tabela_sis_crm_churn)
        dicionario_dados_auditoria = self.transformar_dataframe_dicionario(tabela_churn_silva=tabela_auditoria)
        DBAuditoria().inserir_tb_auditoria(lista_dicionario_dados=dicionario_dados_auditoria)

if __name__ == '__main__':
    Auditoria().rotina_clientes_auditoria()


