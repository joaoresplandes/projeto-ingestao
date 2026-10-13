from Pipeline.Gold.Marketing.Transformacao.UFs.ufs import TransformUFS
from Pipeline.Gold.Marketing.Transformacao.EstadoCivil.estado_civil import TransformEstadoCivil
from Pipeline.Gold.Marketing.Transformacao.Idade.idade import TransformIdade
from Pipeline.Gold.Marketing.Transformacao.Escolaridade.escolaridade import TransformEscolaridade
import polars as pl


class TransformacaoMarketing:
    def __init__(self, tabela_enrriquecida: pl.DataFrame):
        self.__tabela_enrriquecida = tabela_enrriquecida


    def executar(self):
        tabela = TransformUFS(tabela=self.__tabela_enrriquecida).executar()
        tabela = TransformEstadoCivil(tabela=tabela).executar()
        tabela = TransformIdade(tabela=tabela).executar()
        tabela = TransformEscolaridade(tabela=tabela).executar()
        print(tabela.filter(pl.col('desc_escolaridade').is_null()))

