import os


class Path:
    CAMINHO_PADRAO = '\\'.join(os.getcwd().split('\\')[:-4])
    CAMINHO_PROJETO: str = r'Pos_Graduacao_Engenharia_de_Dados\Preparacao_Orquestacao_Fluxo_de_Dados\Unidade02\Materiais\ProjetoChurn'
    FONTE_PROJETO: str = rf"{CAMINHO_PADRAO}\{CAMINHO_PROJETO}\Fonte\SIS_CRM_TB_CHURN.txt"
