from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Gold.Marketing.Enrriquecimento.Escolaridade.escolaridade import Escolaridade
from Pipeline.Gold.Marketing.Enrriquecimento.EstadoCivil.estado_civil import EstadoCivil
from Pipeline.Gold.Marketing.Enrriquecimento.EstadosUF.rotina_mongo import DadosUFS
from Pipeline.Gold.Marketing.Enrriquecimento.MensalidadePerfilCliente.perfil_cliente import RotinaCliente
from Pipeline.Gold.SubRotinasCamada.sub_rotinas_camada import SubRotinasCamada
import polars as pl


class EnrriquecimentoMarketing(RotinaBanco):
    def __init__(self):
        super().__init__()
        self.__nm_marketing_silver: str = 'projeto_churn.silver.tb_churn_marketing'
        self.__nm_marketing_gold: str = 'projeto_churn.gold.tb_churn_marketing'

    def rotina(self) -> pl.DataFrame:
        """
        Rotina de enrriquecimento de dados da tabela de marketing proveniente da cama silver 'tb_churn_marketing' a
        qual a implementados dados das seguintes fontes:
        1 - Dados de Escolaridade
        2 - Dados de Estado Civil
        3 - Dados de Região
        4 - Dados Monetarios de Clientes
        :return: pl.DataFrame com colunas adicionais
        """
        tabela = SubRotinasCamada.selecionar_colunas_entrada(self.tabela(nm_tabela=self.__nm_marketing_silver))
        tabela = Escolaridade(tabela=tabela).executar()
        tabela = EstadoCivil(tabela=tabela).executar()
        tabela = DadosUFS().regiao(tabela_marketing=tabela)
        tabela = RotinaCliente().rotina(tabela=tabela)

        return tabela
