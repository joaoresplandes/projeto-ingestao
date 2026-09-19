from Pipeline.RotinaDuplicados.ValoresDuplicados.valores_duplicados import ValoresDuplicados
from Pipeline.RotinaDuplicados.ValoresNaoDuplicados.valores_sem_duplicados import ValoresNaoDuplicados
from Pipeline.RotinaDuplicados.SubRotinas.sub_rotinas import SubRotinaDuplicados
from Comum.comum import Path
import polars as pl


class RotinaDuplicados:
    def __init__(self, tabela: pl.DataFrame):
        self._tabela = tabela
        self._lista_ids_duplicados = SubRotinaDuplicados.executar(tabela=self._tabela)

    def tabela_sem_duplicados(self) -> pl.DataFrame:
        """
        Executa a rotina de obter a tabela sem os cpfs duplicados
        :return: tabela filtrada sem os ultimos cpfs duplicados
        """
        tabela_sem_duplicados = ValoresNaoDuplicados.filtrar_tabela_sem_duplicados(
            tabela=self._tabela,
            id_duplicatos=self._lista_ids_duplicados
        )

        return tabela_sem_duplicados

    def tabela_com_duplicados(self) -> None:
        """
        Retorna um dataframe com os ultimos registros inseridos de cpfs duplicados
        :return: tabela com os ultimos cpfs duplicados
        """
        tabela_com_duplicados = ValoresDuplicados.filtrar_tabela_duplicados(
            tabela=self._tabela,
            id_duplicatos=self._lista_ids_duplicados
        )

        tabela_com_duplicados.write_excel(
            workbook=rf'{Path.CAMINHO_DESTINO}\CPFS_DUPLICADOS.xlsx',
            worksheet='Duplicados'
        )
        # return tabela_com_duplicados
