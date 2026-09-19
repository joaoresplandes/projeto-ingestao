import polars as pl


class ValoresDuplicados:

    def cpfs_duplicados(self, tabela: pl.DataFrame) -> list:
        """
        Retorna uma lista com todos os cpfs que estão em duplicata na tabela
        :param tabela: DataFrame fonte
        :return:
        """
        lista_cpfs = tabela['cpf'].value_counts().filter(pl.col('count') > 1)['cpf'].to_list()

        return lista_cpfs

    def obter_id_cpf_removidos(self, tabela: pl.DataFrame, lista_cpfs: list) -> list:
        l = sorted([id for id in tabela.filter(pl.col('cpf').is_in(lista_cpfs)).sort('cpf')['id'].unique().to_list()])
        id_duplicatos = l[int(len(l) / 2):]

        return id_duplicatos

    def filtrar_tabela_sem_duplicados(self, tabela: pl.DataFrame, id_duplicatos: list) -> pl.DataFrame:
        tabela_dados_unicos = tabela.filter(~pl.col('id').is_in(id_duplicatos))

        return tabela_dados_unicos