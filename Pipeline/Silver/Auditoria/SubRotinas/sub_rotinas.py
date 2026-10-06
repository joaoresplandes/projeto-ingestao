from Pipeline.Silver.Auditoria.SubRotinas.colunas import ColunasAuditoria
from datetime import datetime
import polars as pl


class TratarAuditoria:
    @staticmethod
    def selecionar_colunas(tabela_auditoria: pl.DataFrame) -> pl.DataFrame:
        """
        Seleciona as colunas iniciais para o tratamento dos dados -> 'id', 'cpf', 'nome', 'sobrenome', 'idgenero',
        'indcliente', 'mes', 'ano'
        :param tabela_auditoria: pl.DataFrame
        :return: pl.DataFrame com colunas reduzidas
        """
        tabela_auditoria = tabela_auditoria.select(ColunasAuditoria.colunas)

        return tabela_auditoria

    @staticmethod
    def coluna_nome_completo(tabela_auditoria: pl.DataFrame) -> pl.DataFrame:
        """
        Concatena as colunas de 'nome' e 'sobrenome' para criar a coluna 'nome_completo'
        :param tabela_auditoria: tabela de dados unicos, sem duplicados
        :return: tabela auditoria filtrada com a nova coluna 'nome_completo'
        """
        tabela_auditoria = tabela_auditoria.with_columns(
            pl.concat_str(
                pl.col('nome'),
                pl.lit(' '),
                pl.col('sobrenome')
            ).alias('nome_completo')
        )

        return tabela_auditoria

    @staticmethod
    def coluna_ano_mes(tabela_auditoria: pl.DataFrame) -> pl.DataFrame:
        """
        Concatena as colunas de 'ano' e 'mes' para criar a coluna 'ano_mes', transformando a coluna em tipo int
        :param tabela_auditoria: tabela de dados unicos, sem duplicados
        :return: tabela auditoria filtrada com a nova coluna 'ano_mes'
        """
        tabela_auditoria = tabela_auditoria.with_columns(
            pl.concat_str(
                pl.col('ano'),
                pl.col('mes')
            ).cast(int).alias('ano_mes')
        )

        return tabela_auditoria

    @staticmethod
    def colunas_finais(tabela_auditoria: pl.DataFrame) -> pl.DataFrame:
        """
        Filtra as colunas finais para inserir os dados no banco
        :param tabela_auditoria: tabela auditoria com todas as colunas criadas
        :return: tabela auditoria com determinadas colunas
        """
        tabela_auditoria = tabela_auditoria.select(ColunasAuditoria.colunas_finais)

        return tabela_auditoria

    @staticmethod
    def coluna_atualizacao_banco(tabela_auditoria: pl.DataFrame) -> pl.DataFrame:
        """
        Coluna de data inserção para informar quando um registro foi atualizado na tabela de auditoria
        :param tabela_auditoria: pl.DataFrame
        :return: pl.DataFrame com as coluna de data_insercao
        """
        tabela_auditoria = tabela_auditoria.with_columns(pl.lit(datetime.now()).alias('data_insercao'))

        return tabela_auditoria

    @staticmethod
    def executar_tratativa_auditoria(tabela_auditoria: pl.DataFrame) -> pl.DataFrame:
        """
        Rotina de tratativa de auditoria para o tramamento da base de auditoria
        :param tabela_auditoria: tabela auditoria filtrada  por indcliente == 1
        :return: tabela com novas colunas e colunas filtradas para inserção em banco de dados
        """
        tabela_auditoria = TratarAuditoria.selecionar_colunas(tabela_auditoria=tabela_auditoria)
        tabela_auditoria = TratarAuditoria.coluna_nome_completo(tabela_auditoria=tabela_auditoria)
        tabela_auditoria = TratarAuditoria.coluna_ano_mes(tabela_auditoria=tabela_auditoria)
        tabela_auditoria = TratarAuditoria.colunas_finais(tabela_auditoria=tabela_auditoria)
        tabela_auditoria = TratarAuditoria.coluna_atualizacao_banco(tabela_auditoria=tabela_auditoria)

        return tabela_auditoria