from Pipeline.Silver.Duplicados.ValoresDuplicados.colunas import ColunasDuplicados
import polars as pl


class ValoresDuplicados:

    @staticmethod
    def selecionar_colunas(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Seleciona as colunas da tabela a envio do relatório
        :param tabela: tabela de dados duplicados
        :return: tabela com colunas filtradas
        """
        tabela = tabela.select(ColunasDuplicados.colunas)

        return tabela

    @staticmethod
    def filtrar_tabela_duplicados(tabela: pl.DataFrame, id_duplicatos: list) -> pl.DataFrame:
        """
        Com a lista de ids de cpfs duplicados, filtra a tabela e mantem apenas os cpfs duplicados que foram inseridos
        no CRM
        :param tabela: tabela original com todos os dados
        :param id_duplicatos: [501, 502, 503, 504, 506, 507]
        :return: tabela com os cpfs duplicados
        """
        tabela_dados_unicos = tabela.filter(pl.col('id').is_in(id_duplicatos)).sort(by='id', descending=True)
        tabela_dados_unicos = ValoresDuplicados.selecionar_colunas(tabela=tabela_dados_unicos)

        return tabela_dados_unicos
