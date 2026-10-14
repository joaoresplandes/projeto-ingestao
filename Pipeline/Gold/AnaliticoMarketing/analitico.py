from Pipeline.Gold.AnaliticoMarketing.banco_dados import DBGold
from BancoDados.rotina_banco import RotinaBanco
import polars as pl


class Analitico(RotinaBanco):
    def __init__(self):
        self.__nm_tb_churn_marketing_gold: str = 'projeto_churn.gold.tb_churn_marketing'
        super().__init__()
        self.__tabela = self.tabela(nm_tabela=self.__nm_tb_churn_marketing_gold)
        self.__tabela = self.__tabela.select(self.__tabela.columns[:-1])

    @staticmethod
    def substituir_escolaridade(valor: str) -> str:
        """
        Substitui os valores de Pós-Graduação, Mestrado, Doutorado por Stricto/Lato Sensu
        :param valor: Mestrado
        :return: Stricto/Lato Sensu
        """
        substituto: str = 'Stricto/Lato Sensu'
        match valor:
            case 'Pós-Graduação':
                return substituto
            case 'Mestrado':
                return substituto
            case 'Doutoradp':
                return substituto
            case _:
                return valor

    @staticmethod
    def faixa_etaria(idade: int) -> str:
        """
        Retorna a classificação de faixa etária conforme a idade de encaixa em um intervalo:
        Até 29 anos – Jovem
        De 30 a 50 anos – Adulto Jovem
        De 51 a 70 anos – Adulto Maduro
        Acima de 70 anos – Idoso
        :param idade: 35
        :return: Adulto Jovem
        """
        if idade > 70:
            return 'Idoso'
        elif 51 <= idade <= 70:
            return 'Adulto Maduto'
        elif 30 <= idade <= 50:
            return 'Adulto Jovem'
        else:
            return 'Jovem'

    def tratatar_colunas(self) -> pl.DataFrame:
        """
        Realiza as devidas tratativas nas colunas de 'escolaridade' e 'idade' criando a coluna de 'faixa_etaria'
        :return: pl.DataFrame
        """
        tabela = self.__tabela.with_columns(
            pl.col('escolaridade')
            .map_elements(self.substituir_escolaridade, return_dtype=pl.Utf8)
        )
        tabela = tabela.with_columns(
            pl.col('idade')
            .map_elements(self.faixa_etaria, return_dtype=pl.Utf8)
            .alias('faixa_etaria')
        )
        return tabela

    @staticmethod
    def agrupar_valores(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza o agrupamento dos dados campos numéricos de acordo com as seguintes colunas:
        gênero,
        UF,
        anomes,
        estado civil,
        escolaridade,
        faixa de idade
        :param tabela: pl.DataFrame
        :return: pl.DataFrame agrupado
        """
        agrupada = tabela.group_by(['genero', 'uf', 'ano_mes', 'estado_civil', 'escolaridade', 'faixa_etaria']).agg(
            pl.col('id').count().alias('total_churn'),
            pl.col('mensalidade').sum().alias('valor_mensalidade_mes'),
            pl.col('participacao').sum().alias('valor_participacao_mes')
        )

        return agrupada

    @staticmethod
    def transformar_dataframe_dicionario(tabela: pl.DataFrame) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela_temp = tabela.with_columns(
            pl.Series([index for index in range(tabela.shape[0])]).alias('index')
        )
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela.columns[:]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados

    def executar(self) -> None:
        """
        Rotina de ingestão da tabela de analitico na camada gold
        :return: None
        """
        tabela = self.tratatar_colunas()
        tabela = self.agrupar_valores(tabela=tabela)
        lista_dicionario_dados = self.transformar_dataframe_dicionario(tabela=tabela)
        if lista_dicionario_dados:
            DBGold().inserir_dados_analiticos(lista_dicionario_dados=lista_dicionario_dados)
