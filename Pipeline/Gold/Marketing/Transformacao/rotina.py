from Pipeline.Gold.Marketing.Transformacao.UFs.ufs import TransformUFS
from Pipeline.Gold.Marketing.Transformacao.EstadoCivil.estado_civil import TransformEstadoCivil
from Pipeline.Gold.Marketing.Transformacao.Idade.idade import TransformIdade
from Pipeline.Gold.Marketing.Transformacao.Escolaridade.escolaridade import TransformEscolaridade
from Pipeline.Gold.Marketing.Transformacao.Mensalidade.mensalidade import TransformMensalidade
from Pipeline.Gold.Marketing.Transformacao.Participacao.participacao import TransformParticipacao
from Pipeline.Gold.SubRotinasCamada.sub_rotinas_camada import SubRotinasCamada
import polars as pl


class TransformacaoMarketing:
    def __init__(self, tabela_enrriquecida: pl.DataFrame):
        self.__tabela_enrriquecida = tabela_enrriquecida


    def executar(self) -> pl.DataFrame:
        """
        Rotina de tratamento de dados da tabela de marketing proveniente da cama silver 'tb_churn_marketing' a
        qual a implementados dados das seguintes fontes:
        1 - Dados de UF
        2 - Dados de Estado Civil
        3 - Dados de Idade
        4 - Dados de Escolaridade
        5 - Dados de Mensalidade
        6 - Dados de Coparticipacao
        :return: pl.DataFrame
        """
        tabela = TransformUFS(tabela=self.__tabela_enrriquecida).executar()
        tabela = TransformEstadoCivil(tabela=tabela).executar()
        tabela = TransformIdade(tabela=tabela).executar()
        tabela = TransformEscolaridade(tabela=tabela).executar()
        tabela = TransformMensalidade(tabela=tabela).executar()
        tabela = TransformParticipacao(tabela=tabela).executar()
        tabela = SubRotinasCamada.colunas_finais_transformacao(tabela=tabela)

        return tabela
