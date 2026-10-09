from Mongo.rotina_mongo import Mongo
import polars as pl


class DadosUFS(Mongo):
    def __init__(self):
        # self.__tabela_marketing = tabela_marketing
        super().__init__()
        self.__colecao: dict = self.obter_dicionario_colecao(nm_colecao='ufs')

    def obter_regiao(self):
        lista_regiao = [
            {uf:dicionario['regiao']} for uf, dicionario in self.__colecao.items()
        ]
        print(lista_regiao)
        pl.DataFrame(

        )


if __name__ == '__main__':
    DadosUFS().obter_regiao()