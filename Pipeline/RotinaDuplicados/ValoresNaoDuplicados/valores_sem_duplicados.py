import polars as pl


class ValoresNaoDuplicados:

    @staticmethod
    def filtrar_tabela_sem_duplicados(tabela: pl.DataFrame, id_duplicatos: list) -> pl.DataFrame:
        """
        Com a lista de ids de cpfs duplicados, filtra a tabela e mantem apenas os cpfs unicos e os primeiros registros
        dos cpfs duplicados
        :param tabela: tabela original com todos os dados
        :param id_duplicatos: [501, 502, 503, 504, 506, 507]
        :return: tabela sem os cpfs duplicados
        """
        tabela_dados_unicos = tabela.filter(~pl.col('id').is_in(id_duplicatos))

        return tabela_dados_unicos