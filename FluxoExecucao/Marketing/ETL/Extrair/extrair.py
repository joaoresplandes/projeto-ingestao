import polars as pl


class Extrair:
    def __init__(self, tabela: pl.DataFrame):
        self._tabela_marketing = tabela
        self._tb_colaboradores_validos = self.filtrar_colaboradores_validos()

    def filtrar_colaboradores_validos(self) -> pl.DataFrame:
        """
        Obtem a tabela sem dados duplicados e filtra apenas os colaboradores ativos -> indcliente == 1
        :return: tabela filtrada com indcliente == 1
        """
        tabela_mkt = self._tabela_marketing.filter(pl.col('indcliente') != 1)
        return tabela_mkt

    def executar(self) -> pl.DataFrame:
        """
        Executa o rotina de extração da tabela mkt
        :return: tabela mkt filtrada
        """
        return self._tb_colaboradores_validos