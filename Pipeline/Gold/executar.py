from Pipeline.Gold.Auditoria.clientes_auditados import Auditoria
from Pipeline.Gold.Marketing.rotina_marketing import RotinaMarketing
from Pipeline.Gold.AnaliticoMarketing.analitico import Analitico


class RotinaGold:

    @staticmethod
    def executar() -> None:
        """
        Executa o processo de ingestão da camada gold
        :return: None
        """
        Auditoria().rotina_auditoria()
        RotinaMarketing().executar()
        Analitico().executar()
