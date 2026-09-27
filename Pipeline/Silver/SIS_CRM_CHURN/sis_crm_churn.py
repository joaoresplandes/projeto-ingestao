from Pipeline.Silver.SIS_CRM_CHURN.fluxo_db_sis_crm_churn import DBCrmChur
import polars as pl


class SilverSisCrmChurn:
    def __init__(self):
        self.__tabela_completa = DBCrmChur().tb_sis_crm_churn_bronze()


    def transformar_dataframe_dicionario(self) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela = self.__tabela_completa
        tabela_temp = tabela.with_columns(pl.Series([index for index in range(tabela.shape[0])]).alias('index'))
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela.columns[:-1]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados


if __name__ == '__main__':
    SilverSisCrmChurn().transformar_dataframe_dicionario()

