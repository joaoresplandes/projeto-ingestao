import polars as pl


class ValoresDuplicados:

    def cpfs_duplicados(self, tabela: pl.DataFrame) -> list:
        """
        Retorna uma lista com todos os cpfs que estão em duplicata na tabela
        :param tabela: DataFrame fonte
        :return: ['34567800223','45656709989', '12345678901', '45656719989', '46178257774', '45656729989']
        """
        lista_cpfs = tabela['cpf'].value_counts().filter(pl.col('count') > 1)['cpf'].to_list()

        return lista_cpfs

    @staticmethod
    def obter_id_cpf_removidos(tabela: pl.DataFrame, lista_cpfs: list) -> list:
        """
        Retorna os ids dos cpfs duplicados, mas retorna apenas os ultimos ids criados autimaticamente pelo sistema de
        CRM para que os primeiros registros inseridos sejam mantidos
        :param tabela: tabela de dados duplicados
        :param lista_cpfs: lista de cpfs duplicados
        :return: [501, 502, 503, 504, 506, 507]
        """
        l = sorted([id for id in tabela.filter(pl.col('cpf').is_in(lista_cpfs)).sort('cpf')['id'].unique().to_list()])
        id_duplicatos = l[int(len(l) / 2):]

        return id_duplicatos

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