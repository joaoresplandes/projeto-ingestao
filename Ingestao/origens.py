from os import getcwd


class PathBasesComplementares:

    PATH_BASE: str = '/'.join(getcwd().split('/')[:-3])
    PATH_ORQUESTACAO: str = rf'{PATH_BASE}/PosGraduacaoEngenhariaDados/14_Preparacao_Orquestacao_Fluxo_de_Dados'
    UNIDADE_TRES: str = rf'{PATH_ORQUESTACAO}/Unidade03/Materiais'
    ARQUIVO_ESTADO_CIVIL: str = rf"{UNIDADE_TRES}/estadocivil.json"
    ARQUIVO_ESCOLARIDADE: str = rf"{UNIDADE_TRES}/escolaridade.txt"