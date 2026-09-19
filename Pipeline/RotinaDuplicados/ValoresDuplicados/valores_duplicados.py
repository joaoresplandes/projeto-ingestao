import polars as pl


class ValoresDuplicados:

    @staticmethod
    def filtrar_tabela_duplicados(tabela: pl.DataFrame, id_duplicatos: list) -> pl.DataFrame:
        """
        Com a lista de ids de cpfs duplicados, filtra a tabela e mantem apenas os cpfs duplicados que foram inseridos
        no CRM
        :param tabela: tabela original com todos os dados
        :param id_duplicatos: [501, 502, 503, 504, 506, 507]
        :return: tabela com os cpfs duplicados
        """
        tabela_dados_unicos = tabela.filter(pl.col('id').is_in(id_duplicatos))

        return tabela_dados_unicos
