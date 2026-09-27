from FluxoExecucao.ClientesAtivosAuditoria.TratarAuditoria.tratar_auditoria import TratarAuditoria
from BancoDados.rotina_banco import BancoDados
import polars as pl


class ClientesAuditoria:
    @staticmethod
    def filtrar_clientes_auditoria(tabela_dados_unicos: pl.DataFrame) -> None:
        """
        Filta a tabela pela coluna IndCliente, o que determina os clientes a serem analisados pelo time de auditoria
        :param tabela_dados_unicos: tabela de dados unicos, sem duplicados
        :return: tabela filtrada pelo indcliente == 1
        """
        tabela_auditoria = tabela_dados_unicos.filter(pl.col('indcliente') == 1)
        tabela_auditoria = TratarAuditoria.executar_tratativa_auditoria(tabela_auditoria=tabela_auditoria)
        BancoDados().inserir_dados(tabela_dados=tabela_auditoria)
