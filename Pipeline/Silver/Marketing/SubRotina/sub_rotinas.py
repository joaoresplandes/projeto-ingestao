# from FluxoExecucao.Marketing.ETL.Transformar.colunas import ColunasMKT
import polars as pl


class SubRotinas:

    @staticmethod
    def criar_coluna_anomes(tabela_mkt: pl.DataFrame) -> pl.DataFrame:
        """
        Cria uma coluna chamada 'ano_mes' concatenando as colunas 'ano' e 'mes', transformando a coluna em tipo int
        :param tabela_mkt: tabela filtrada com indcliente == 1
        :return: tabela com coluna adicional 'ano_mes'
        """
        tabela_mkt = tabela_mkt.with_columns(
            pl.concat_str(
                pl.col('ano'),
                pl.col('mes')
            ).cast(int).alias('ano_mes')
        )

        return tabela_mkt

    @staticmethod
    def tratar_colunas(tabela_mkt: pl.DataFrame) -> pl.DataFrame:
        """
        Para cada uma das colunas abaixo, são transformadas para tipo 'int' e renomeadas:
        1° estado_civil -> codestadocivil
        2° idade -> idade
        3° escolaridade -> codescolaridade
        :param tabela_mkt: tabela com apenas funcionarios ativos
        :return: tabela com apenas funcionarios ativos e novas colunas de 'codestadocivil' e 'codescolaridade'
        """
        tabela_mkt = tabela_mkt.with_columns(pl.col('estado_civil').cast(int).alias('codestadocivil'))
        tabela_mkt = tabela_mkt.with_columns(pl.col('idade').cast(int).alias('idade'))
        tabela_mkt = tabela_mkt.with_columns(pl.col('escolaridade').cast(int).alias('codescolaridade'))

        return tabela_mkt

    @staticmethod
    def colunas_mkt(tabela_mkt: pl.DataFrame) -> pl.DataFrame:
        """
        filtra apenas as colunas que sejam necessarias para o arquivo final informado pelo time de marketing
        :param tabela_mkt: tabela completa de funcionarios ativos
        :return: tabela com colunas filtradas
        """
        tabela_mkt = tabela_mkt.select(
            [
                'id',
                'idgenero',
                'codestadocivil',
                'idade',
                'uf',
                'codescolaridade',
                'indcliente',
                'ano_mes'
            ]
        )

        return tabela_mkt

    def executar(self, tabela_mkt: pl.DataFrame) -> pl.DataFrame:
        """
        Executa a rotina da colasse Transformar
        :param tabela_mkt: tabela mkt filtrada
        :return: tabela mkt pronta para exportação
        """
        tabela_mkt = self.criar_coluna_anomes(tabela_mkt=tabela_mkt)
        tabela_mkt = self.tratar_colunas(tabela_mkt=tabela_mkt)
        tabela_mkt = self.colunas_mkt(tabela_mkt=tabela_mkt)

        return tabela_mkt
