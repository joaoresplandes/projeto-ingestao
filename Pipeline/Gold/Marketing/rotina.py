from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Gold.Marketing.Escolaridade.escolaridade import Escolaridade
from Pipeline.Gold.Marketing.EstadoCivil.estado_civil import EstadoCivil
from Pipeline.Gold.SubRotinasCamada.sub_rotinas_camada import SubRotinasCamada


class MarketingGold(RotinaBanco):
    def __init__(self):
        super().__init__()
        self.__nm_marketing_silver: str = 'projeto_churn.silver.tb_churn_marketing'
        self.__nm_marketing_gold: str = 'projeto_churn.gold.tb_churn_marketing'

    def rotina(self):
        tabela_silver = SubRotinasCamada.selecionar_colunas_entrada(self.tabela(nm_tabela=self.__nm_marketing_silver))
        tabela_silver_escolaridade = Escolaridade(tabela=tabela_silver).executar()
        tabela_silver_estado_civil = EstadoCivil(tabela=tabela_silver_escolaridade).executar()

if __name__ == '__main__':
    MarketingGold().rotina()
