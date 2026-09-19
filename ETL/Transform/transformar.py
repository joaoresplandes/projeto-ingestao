import polars as pl
from unidecode import unidecode
import re


class Tratativas:
    def __init__(self):
        self._mapeamento = {
            r'\b(masculino|masc|m)\b': 'M',
            r'\b(bigenero|bi|b)\b': 'B',
            r'\b(feminino|fem|fe|f)\b': 'F',
            r'\b(agenero|ag|a)\b': 'A',
            r'\b(outros|outro|o)\b': 'O'
        }

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

    def criar_dataframe(self, dict_tabela: dict) -> pl.DataFrame:
        """
        Cria o DataFrame a partir do dicionario de dados já tratado
        :param dict_tabela: dicionario de dados tratado
        :return: DataFrame com os dados tratado
        """
        tabela = pl.DataFrame(dict_tabela)

        return tabela
