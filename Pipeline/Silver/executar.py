from Pipeline.Silver.Duplicados.duplicados import RotinaDuplicados
from Pipeline.Silver.SisCrmChurn.sis_crm_churn import SilverSisCrmChurn
from Pipeline.Silver.Marketing.marketing import Marketing

class RotinaSilver:

    @staticmethod
    def executar() -> None:
        """
        Executa o processo de ingestão da camada silver
        :return: None
        """
        SilverSisCrmChurn().executar()
        RotinaDuplicados().rotina_principal()
        Marketing().rotina()


if __name__ == '__main__':
    RotinaSilver().executar()
