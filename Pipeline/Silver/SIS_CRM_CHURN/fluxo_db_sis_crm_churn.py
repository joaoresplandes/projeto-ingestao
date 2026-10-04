from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
import polars as pl


class DBCrmChur(RotinaBanco):
    def __init__(self):
        self.__nm_tb_sis_crm_churn_silver: str = 'projeto_churn.silver.tb_sis_crm_churn'
        super().__init__(nome_tabela=self.__nm_tb_sis_crm_churn_silver)

