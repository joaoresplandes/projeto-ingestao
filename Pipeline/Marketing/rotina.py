from Pipeline.Marketing.ETL.Extrair.extrair import Extrair
from Pipeline.Marketing.ETL.Transformar.transformar import Transformar
from Pipeline.Marketing.ETL.Carregar.carregar import Carregar
import polars as pl


class Rotina:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela_mkt = tabela

    def executar(self) -> None:
        """
        Rotina de execução do Pipeline de ETL da rotina de Marketing
        :return: None
        """
        tabela_mkt = Extrair(tabela=self.__tabela_mkt).executar()
        tabela_mkt = Transformar().executar(tabela_mkt=tabela_mkt)
        Carregar().executar(tabela_mkt=tabela_mkt)
