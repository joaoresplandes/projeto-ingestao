from Pipeline.Silver.Ingestao.ingestao import CamadaBronze
from unidecode import unidecode
import polars as pl
import re


class SilverSisCrmChurn:
    def __init__(self):
        self.__tabela_completa = CamadaBronze().tb_sis_crm_churn_bronze()
        self._mapeamento = {
            r'\b(masculino|masc|m)\b': 'M',
            r'\b(bigenero|bi|b)\b': 'B',
            r'\b(feminino|fem|fe|f)\b': 'F',
            r'\b(agenero|ag|a)\b': 'A',
            r'\b(outros|outro|o)\b': 'O'
        }

    @property
    def tabela_completa(self):
        return self.__tabela_completa

    def transformar_dataframe_dicionario(self) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela = self.__tabela_completa
        tabela_temp = tabela.with_columns(pl.Series([index for index in range(tabela.shape[0])]).alias('index'))
        lista_dados = [
            {
                coluna: tabela_temp.filter(pl.col('index') == indice_linha)[coluna].to_list()[0]
                for coluna in tabela.columns[:-1]
            }
            for indice_linha in tabela_temp['index'].to_list()
        ]
        return lista_dados

    def tratar_genero(self, texto: str) -> str:
        """
        Com uma função regex, reconhece o padrão no valor de cada linha da coluna e retorna o valor correspondente de
        mapeamento
        :param texto: texto a ser compradado -> coluna genero
        :return: M, B, F, A, O
        """
        texto = unidecode(texto).lower()
        for padrao, valor in self._mapeamento.items():
            texto = re.sub(padrao, valor, texto, flags=re.IGNORECASE | re.VERBOSE)
        return texto

    def tratar_colunas(self, dict_tabela: dict) -> dict:
        """
        Tratando cada uma das respectivas decolunas de acordo com cada especialidade:
        1° CPF -> Retirar '.' e '-'
        2° GENERO -> Usa ReGex para encontrar um padrão no texto e retonar a categoria correta
        3° ID -> Transforma o tipo de dados que antes era String para Int
        4° IndCliente -> Transforma o valor que antes era String para Int e caso encontre um valor Null, converte
        para 0 (Zero)
        :param dict_tabela: dicionario de dados ja estruturado
        :return:dicionario de dados ja estruturado tratado
        """
        dict_tabela['cpf'] = [cpf.replace('.', '').replace('-', '') for cpf in dict_tabela['cpf']]
        dict_tabela['idgenero'] = [self.tratar_genero(texto=genero) for genero in dict_tabela['idgenero']]
        dict_tabela['ID'] = [int(id) for id in dict_tabela['ID']]
        dict_tabela['indcliente'] = [int(indcliente) if indcliente != '' else 0 for indcliente in dict_tabela['indcliente']]

        return dict_tabela

    @staticmethod
    def criar_dataframe(dict_tabela: dict) -> pl.DataFrame:
        """
        Cria o DataFrame a partir do dicionario de dados já tratado
        :param dict_tabela: dicionario de dados tratado
        :return: DataFrame com os dados tratado
        """
        tabela = pl.DataFrame(dict_tabela)

        return tabela

    def executar(self, dicionario_tabela: dict) -> pl.DataFrame:
        """
        Rotina de tratamento de dados da fonte inicial .txt
        :param dicionario_tabela: dicionario de dados tratado
        :return: DataFrame com os dados tratado
        """
        dicionario_tabela = self.tratar_colunas(dict_tabela=self.transformar_dataframe_dicionario())
        tabela = self.criar_dataframe(dict_tabela=dicionario_tabela)

        return tabela


if __name__ == '__main__':
    print(SilverSisCrmChurn().executar())

