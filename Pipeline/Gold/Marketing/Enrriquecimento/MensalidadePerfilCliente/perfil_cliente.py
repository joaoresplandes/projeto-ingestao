from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Gold.Marketing.Enrriquecimento.MensalidadePerfilCliente.Transform.transform import Transform
import polars as pl


class RotinaCliente(RotinaBanco):
    def __init__(self):
        self.__nm_perfil_churn_cliente: str = 'projeto_churn.bronze.tb_perfil_cliente tpc'
        super().__init__()

    def obter_perfil_cliente(self) -> pl.DataFrame:
        tabela = self.tabela(nm_tabela=self.__nm_perfil_churn_cliente)
        tabela = Transform.tratar_coluna_decimal(tabela=tabela, nm_coluna='vlr_mensal')
        tabela = Transform.tratar_coluna_decimal(tabela=tabela, nm_coluna='vlr_coparticipacao')
        tabela = Transform.filtrar_colunas(tabela=tabela)

        return tabela

    def rotina(self, tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Rotina de unir a tabela principal de marketing com a tabela de 'perfil_cliente' para obter os campos de
        'vlr_mensal' e 'vlr_coparticipacao'
        :param tabela: pl.DataFrame -> tabela de marketing
        :return: pl.DataFrame -> tabela de marketing com as colunas 'vlr_mensal' e 'vlr_coparticipacao' adicionadas
        """
        tabela_perfil_cliente = self.obter_perfil_cliente()
        tabela_resultado = tabela.join(
            tabela_perfil_cliente,
            left_on='id',
            right_on='id',
            how='left'
        )

        return tabela_resultado


if __name__ == '__main__':
    RotinaCliente().obter_perfil_cliente()


