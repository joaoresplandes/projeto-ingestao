from Pipeline.Bronze.Escolaridade.escolaridade import IngestaoEscolaridade
from Pipeline.Bronze.EstadoCivil.estado_civil import IngestaoEstadoCivil
from Pipeline.Bronze.SisCrmChurn.sis_crm_churn import BronzeSisCrmChurn
from Pipeline.Bronze.MongoDBUFS.rotina_ufs import RotinaMongo


class RotinaBronze:

    @staticmethod
    def executar() -> None:
        """
        Executa o processo de ingestão da camada bronze
        :return: None
        """
        IngestaoEscolaridade().rotina()
        IngestaoEstadoCivil().rotina()
        RotinaMongo().rotina_ufs_mongo()
        BronzeSisCrmChurn().rotina()
