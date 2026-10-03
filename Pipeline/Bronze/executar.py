from Pipeline.Bronze.Escolaridade.escolaridade import IngestaoEscolaridade
from Pipeline.Bronze.EstadoCivil.estado_civil import IngestaoEstadoCivil
from Pipeline.Bronze.SIS_CRM_CHURN.sis_crm_churn import BronzeSisCrmChurn
from Pipeline.Bronze.MongoDB.rotina import RotinaMongo


class RotinaBronze:

    @staticmethod
    def executar():
        """
        Executa o processo de ingestão da camada bronze
        :return:
        """
        IngestaoEscolaridade().rotina()
        IngestaoEstadoCivil().rotina()
        RotinaMongo().rotina_atualizar()
        BronzeSisCrmChurn().rotina()


if __name__ == '__main__':
    RotinaBronze.executar()