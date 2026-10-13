import polars as pl


class TransformEstadoCivil:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela


    def filtrar_tabela_sem_vazios(self):
        """
        Filtra a tabela pela coluna 'estado_civil' com dados não nulos
        :return: pl.DataFrame com dados não null
        """
        tabela_filtro = self.__tabela.filter(~pl.col('dsc_ec').is_null())

        return tabela_filtro

    def obter_moda(self) -> str:
        """
        Retorna a moda da coluna de 'dsc_ec' que representa o estado civil
        :return: 'Solteiro(a)'
        """
        moda = self.__tabela['dsc_ec'].mode()[0]

        return moda

    def filtrar_tabela_vazios(self) -> pl.DataFrame:
        """
        Filtra os dados da coluna 'dsc_ec' que representa o estado civil como null e substituindo esses valores null
        pela moda da própria coluna
        :return: pl.DataFrame com as 'dsc_ec' alterada para a moda
        """
        tabela_filtrar = self.__tabela.filter(pl.col('dsc_ec').is_null())

        return tabela_filtrar.with_columns(pl.lit(self.obter_moda()).alias('dsc_ec'))

    @staticmethod
    def tabela_completa(tb_nao_vazio: pl.DataFrame, tb_vazio: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza a concatenacao da tabela 'tb_nao_vazio' com os dados de 'dsc_ec' sem alteracao e da tabela 'tb_vazio'
        alterados de vazio para a moda
        :param tb_nao_vazio: tabela com dsc_ec sem alteracao
        :param tb_vazio: tabela com dados de dsc_ec alterados pela moda
        :return: pl.DataFrame -> tabela completa
        """
        tabela_resultado = pl.concat(
            [
                tb_nao_vazio,
                tb_vazio
            ]
        )

        return tabela_resultado


    def executar(self) -> pl.DataFrame:
        """
        Retorna a tabela com os tratamentos de estado civil
        :return: pl.DataFrame tratado
        """
        tabela_nao_vazios = self.filtrar_tabela_sem_vazios()
        tabela_vazio = self.filtrar_tabela_vazios()

        return self.tabela_completa(tb_nao_vazio=tabela_nao_vazios, tb_vazio=tabela_vazio)