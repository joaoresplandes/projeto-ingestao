from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Gold.SubRotinasCamada.sub_rotinas_camada import SubRotinasCamada
import polars as pl


class Escolaridade(RotinaBanco):
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela
        self.__nm_db_escolaridade: str = 'projeto_churn.bronze.tb_escolaridade'
        super().__init__()

    def complementar_tabela_original(self, tabela_escolaridade: pl.DataFrame ) -> pl.DataFrame:
        """
        Com a tabela escolaridade, complementa com os seus dados a tabela original através das colunas de
        'codescolaridade' e 'id_escolatidade', assim enrriquecendo a tabela original com mais informações de escolaridade
        :param tabela_escolaridade: DataFrame de escolaridade
        :return: tabela de marketing com informações complementares de estado civil
        """
        tabela_mkt = self.__tabela.join(
            SubRotinasCamada.selecionar_colunas_entrada(tabela_escolaridade),
            left_on='codescolaridade',
            right_on='id_escolaridade',
            how='left'
        )

        return tabela_mkt

    def executar(self) -> pl.DataFrame:
        """
        Executa o processo de enrriquecimento de informações referente a estado civil
        :return: tabela original complementada com informações de estado civil
        """
        tb_escolaridade = self.tabela(nm_tabela=self.__nm_db_escolaridade)
        tabela_final = self.complementar_tabela_original(tabela_escolaridade=tb_escolaridade)

        return tabela_final
