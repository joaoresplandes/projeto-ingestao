from Comum.comum import Path
import polars as pl


class Carregar:
    def __init__(self):
        self.__path = Path.CAMINHO_DESTINO

    def exportar_base(self, tabela_mkt: pl.DataFrame) -> None:
        """
        Exportar a tabela 'tabela_mkt' como arquivo .csv -> 1-CHURN_PARFIL.csv -> para o diretori de destino
        :param tabela_mkt: tabela final tratata
        :return: None
        """
        tabela_mkt.write_csv(Rf'{self.__path}\1-CHURN_PERFIL.csv', separator=';')

    def executar(self, tabela_mkt: pl.DataFrame) -> None:
        """
        Executa o processo de exportação da tabela mkt
        :param tabela_mkt: tabela mkt pronta e tratada
        :return: NOne
        """
        self.exportar_base(tabela_mkt=tabela_mkt)
