from os import getcwd


class Path:

    PATH_BASE: str = '/'.join(getcwd().split('/')[:4])
    CAMINHO_PROJETO: str = r'PosGraduacaoEngenhariaDados/14_Preparacao_Orquestacao_Fluxo_de_Dados'
    UNIDADE_DOIS: str = rf'{CAMINHO_PROJETO}/Unidade02/Materiais/ProjetoChurn'
    PATH_ORQUESTACAO: str = rf'{PATH_BASE}/PosGraduacaoEngenhariaDados/14_Preparacao_Orquestacao_Fluxo_de_Dados'
    UNIDADE_TRES: str = rf'{PATH_ORQUESTACAO}/Unidade03/Materiais'
    ARQUIVO_ESTADO_CIVIL: str = rf"{UNIDADE_TRES}/estadocivil.json"
    ARQUIVO_ESCOLARIDADE: str = rf"{UNIDADE_TRES}/escolaridade.txt"
    FONTE_PROJETO: str = rf"{PATH_BASE}/{UNIDADE_DOIS}/Fonte/SIS_CRM_TB_CHURN.txt"
    CAMINHO_DESTINO: str = rf"{PATH_BASE}/{UNIDADE_DOIS}/Destino"


