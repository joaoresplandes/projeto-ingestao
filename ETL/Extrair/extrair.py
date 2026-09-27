from Comum.comum import Path
from unidecode import unidecode
from pprint import pprint


class Extrair:
    def __init__(self):
        self.path_arquivo = Path.FONTE_PROJETO

    def extrair_arquivo(self) -> list:
        """
        Com o método with, carrega o conteudo do arquivo .txt no codigo
        :return: string dos dados carregados
        """
        with open(self.path_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = arquivo.readlines()

        return dados

    @staticmethod
    def obter_conjunto_dados(dados: list) -> list:
        """
        Converte os dados em string estrurados em listas, com a primeira sendo o titulo das colunas e as demais listas
        sendo os dados da tabela
        :param dados: dados em string
        :return: lista de dados estruturados
        """
        conjunto = [
            [valor.strip() for valor in linha.replace('\t', ',').replace('\n', '').split(',')]
            for linha in dados
        ]

        return conjunto

    @staticmethod
    def tratar_colunas(lista_colunas: list) -> list:
        """
        Transforma todos dos valores da coluna em caixa baixa com o método .lower()
        :param lista_colunas: lista de colunas com tamanhos variados
        :return: lista de colunas com todos os valores em caixa baixa
        """
        lista_colunas = [unidecode(coluna).lower() for coluna in lista_colunas]

        return lista_colunas

    def dicionario_dados(self, conjunto_dados: list) -> dict:
        """
        Com os dados separados em linhas por listas, é possível criar uma estrutura de dicionario com cada um dos
        valores da primiera lista com chaves e seus respectivos valores em sua lista de valores, respectivo a posição
        atual de cada uma das demais listas
        :param conjunto_dados: listas de dados
        :return: dicionarios de chaves sendo cada um dos valores da primeira lista e seus respectivos valores em lista
        """
        dict_tabela = {}
        for i, coluna in enumerate(self.tratar_colunas(conjunto_dados[0])):
            lista_dados = []
            for dado in conjunto_dados[1:]:
                lista_dados.append(dado[i].upper())
            dict_tabela[coluna] = lista_dados

        return dict_tabela

    def executar(self) -> dict:
        """
        Função que executa todas as etapas sequenciais de extração dos dados do arquivo .txt inicial
        :return: dicionario de dados tratado
        """
        dados = self.extrair_arquivo()
        lista_dados = self.obter_conjunto_dados(dados=dados)
        dicionario_tabela = self.dicionario_dados(conjunto_dados=lista_dados)

        return dicionario_tabela


if __name__ == '__main__':
    print(Extrair().executar())