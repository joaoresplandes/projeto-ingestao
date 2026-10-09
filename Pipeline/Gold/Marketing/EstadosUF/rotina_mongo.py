from polars import row_index

from Mongo.rotina_mongo import Mongo
import polars as pl


class DadosUFS(Mongo):
    def __init__(self):
        super().__init__()
        self.__colecao: dict = self.obter_dicionario_colecao(nm_colecao='ufs')

    def obter_regiao(self) -> pl.DataFrame:
        """
        Obtem os dados da colecao 'ufs' da tabela 'db_projeto_churn' do mongodb e transforma em um dataframe
        :return: pl.DataFrame com dados de UF e Região
        """
        lista_regiao = [
            (uf, dicionario['regiao']) for uf, dicionario in self.__colecao.items()
        ]
        tb_regiao = pl.DataFrame(
            lista_regiao,
            schema=['uf', 'regiao'],
            orient='row'
        )

        return tb_regiao

    def coluna_regiao(self, tabela_marketing: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza um inner join da tabela 'tabela_marketing' com a tabela de 'tb_regiao' para que a tabela de marketing
        possa ser as informações de região em sua principal
        :param tabela_marketing: pl.DataFrame -> tabela de marketing
        :return: pl.DataFrane -> tabela de marketing com a coluna de regiao adicional
        """
        tabela_resultado = tabela_marketing.join(
            self.obter_regiao(),
            left_on='uf',
            right_on='uf',
            how='left'
        )

        return tabela_resultado


if __name__ == '__main__':
    print(DadosUFS().obter_regiao())