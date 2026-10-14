from Pipeline.Gold.Marketing.Enrriquecimento.rotina import EnrriquecimentoMarketing
from Pipeline.Gold.Marketing.Transformacao.rotina import TransformacaoMarketing


class RotinaMarketing:

    @staticmethod
    def executar():
        tabela = EnrriquecimentoMarketing().rotina()
        tabela = TransformacaoMarketing(tabela_enrriquecida=tabela).executar()
        print(tabela)


if __name__ == '__main__':
    RotinaMarketing().executar()