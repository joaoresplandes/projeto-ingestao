from Pipeline.Silver.RotinaBancoSilver import RotinaBanco


class BancoAuditoria(RotinaBanco):
    def __init__(self):
        self.__nm_tabela_banco = r'projeto_churn.silver.tb_cliente_churn_auditoria'
        super().__init__(nome_tabela=self.__nm_tabela_banco)