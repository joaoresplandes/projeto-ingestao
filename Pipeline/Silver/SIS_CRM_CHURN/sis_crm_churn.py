from Pipeline.Silver.RotinaBancoSilver import RotinaBanco
from Pipeline.Silver.Ingestao.ingestao import CamadaBronze
from unidecode import unidecode
import polars as pl
import re


class SilverSisCrmChurn(RotinaBanco):
    def __init__(self):

        self.__nm_tabela_churn_bronze = CamadaBronze().tb_sis_crm_churn_bronze()
        self.__nm_tabela_churn_silver = 'projeto_churn.silver.tb_sis_crm_churn'
        self._mapeamento = {
            r'\b(masculino|masc|m)\b': 'M',
            r'\b(bigenero|bi|b)\b': 'B',
            r'\b(feminino|fem|fe|f)\b': 'F',
            r'\b(agenero|ag|a)\b': 'A',
            r'\b(outros|outro|o)\b': 'O'
        }
        super().__init__(nome_tabela=self.__nm_tabela_churn_silver)

    @property
    def tabela_completa(self):
        return self.__tabela_completa

    def transformar_dataframe_dicionario(self) -> list:
        """
        Transforma uma tabela proveniente de um banco de dados que vem em pl.DataFrame, em uma lista de dicionario de
        dados
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        tabela = self.__nm_tabela_churn_bronze
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

    def tratar_colunas(self, list_dict_tabela: list) -> list:
        """
        Tratando cada uma das respectivas decolunas de acordo com cada especialidade:
        1° CPF -> Retirar '.' e '-'
        2° GENERO -> Usa ReGex para encontrar um padrão no texto e retonar a categoria correta
        3° ID -> Transforma o tipo de dados que antes era String para Int
        4° IndCliente -> Transforma o valor que antes era String para Int e caso encontre um valor Null, converte
        para 0 (Zero)
        :param list_dict_tabela: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return:dicionario de dados ja estruturado tratado
        """
        list_dict_tabela_saida = []
        for dict_tabela in list_dict_tabela:
            dict_tabela['id'] = int(dict_tabela['id'])
            dict_tabela['cpf'] = int(dict_tabela['cpf'].replace('.', '').replace('-', ''))
            dict_tabela['idgenero'] = self.tratar_genero(texto=dict_tabela['idgenero'])
            dict_tabela['estado_civil'] = int(dict_tabela['estado_civil'])
            dict_tabela['idade'] = int(dict_tabela['idade'])
            dict_tabela['escolaridade'] = int(dict_tabela['escolaridade'])
            dict_tabela['indcliente'] = int(dict_tabela['indcliente']) if dict_tabela['indcliente'] != '' else 0

            list_dict_tabela_saida.append(dict_tabela)

        return list_dict_tabela_saida

    @staticmethod
    def obter_ids_bronze(lista_dicionario_dados: list) -> list:
        """
        Retorna uma lista de ids da tabela crm churn proveniente da camana bronze
        :param lista_dicionario_dados: [{'id': 1, 'cpf': 12345678901, 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...]
        """
        lista_ids_bronze = [dicionario['id'] for dicionario in lista_dicionario_dados]
        
        return lista_ids_bronze

    @staticmethod
    def criar_dataframe(dict_tabela: dict) -> pl.DataFrame:
        """
        Cria o DataFrame a partir do dicionario de dados já tratado
        :param dict_tabela: dicionario de dados tratado
        :return: DataFrame com os dados tratado
        """
        tabela = pl.DataFrame(dict_tabela)

        return tabela

    def executar(self):
        """
        Rotina de tratamento de dados da fonte inicial .txt
        :param dicionario_tabela: dicionario de dados tratado
        :return: DataFrame com os dados tratado
        """
        lista_dados = self.transformar_dataframe_dicionario()
        lista_dicionario_tabela = self.tratar_colunas(list_dict_tabela=lista_dados)
        ids_churn_silver = self.ids_sis_crm_churn_silver()
        ids_churn_bronze = self.obter_ids_bronze(lista_dicionario_tabela)


        # tabela = self.criar_dataframe(dict_tabela=dicionario_tabela)

        return lista_dicionario_tabela


if __name__ == '__main__':
    lista_dicionario = SilverSisCrmChurn().executar()
    print(lista_dicionario[0])
    for chave, valor in lista_dicionario[0].items():
        print(f'chave: {chave} - valor: {valor} - tipo dado -> {type(valor)}')

