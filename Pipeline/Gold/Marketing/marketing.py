from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
import polars as pl


class Marketing(RotinaBanco):
    def __init__(self):
        self.__nm_tb_sis_crm_churn_silver: str = 'perfil_churn.silver.tb_sis_crm_churn'
        super().__init__()

    def filtrar_colaboradores_validos(self) -> pl.DataFrame:
        """
        Obtem a tabela sem dados duplicados e filtra apenas os colaboradores ativos -> indcliente == 1
        :return: tabela filtrada com indcliente != 1
        """
        tabela_mkt = self.tb_camada_silver(self.__nm_tb_sis_crm_churn_silver).filter(pl.col('indcliente') != 1)

        return tabela_mkt