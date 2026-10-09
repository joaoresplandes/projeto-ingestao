from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Gold.SubRotinasCamada.sub_rotinas_camada import SubRotinasCamada
import polars as pl


class EstadoCivil(RotinaBanco):
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela
        self.__nm_db_escolaridade: str = 'projeto_churn.bronze.tb_estado_civil'
        super().__init__()

    def complementar_tabela_original(self, tabela_estado_civil: pl.DataFrame ) -> pl.DataFrame:
        """
        Com a tabela estado civil, complementa com os seus dados a tabela original através das colunas de
        'codestadocivil' e 'id_ec', assim enrriquecendo a tabela original com mais informações de estado civil
        :param tabela_estado_civil: DataFrame de estado civil
        :return: tabela de marketing com informações complementares de estado civil
        """
        tabela_mkt = self.__tabela.join(
            SubRotinasCamada.selecionar_colunas_entrada(tabela_estado_civil),
            left_on='codestadocivil',
            right_on='id_ec',
            how='left'
        )

        return tabela_mkt

    def executar(self) -> pl.DataFrame:
        """
        Executa o processo de enrriquecimento de informações referente a estado civil
        :return: tabela original complementada com informações de estado civil
        """
        tb_estado_civil = self.tabela(nm_tabela=self.__nm_db_escolaridade)
        tabela_final = self.complementar_tabela_original(tabela_estado_civil=tb_estado_civil)

        return tabela_final
