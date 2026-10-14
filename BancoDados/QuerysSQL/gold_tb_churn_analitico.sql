create table projeto_churn.gold.tb_churn_analitico(
		genero varchar(1) not null,
		uf varchar(2) not null,
		ano_mes int not null,
		estado_civil varchar(50) not null,
		escolaridade varchar(50) not null,
		faixa_etaria varchar(50) not null,
		total_churn int not null,
		valor_mensalidade_mes int not null,
		valor_participacao_mes int not null,
		data_insercao varchar(30) not null
);