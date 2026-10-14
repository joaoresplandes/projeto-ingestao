from Pipeline.Gold.Marketing.Enrriquecimento.rotina import EnrriquecimentoMarketing
from Pipeline.Gold.Marketing.Transformacao.rotina import TransformacaoMarketing
from Pipeline.Gold.Marketing.DBMarketing.fluxo_marketing import FluxoBanco


class RotinaMarketing:

    @staticmethod
    def executar():
        tabela = EnrriquecimentoMarketing().rotina()
        tabela = TransformacaoMarketing(tabela_enrriquecida=tabela).executar()
        FluxoBanco(tabela=tabela).executar()


if __name__ == '__main__':
    RotinaMarketing().executar()