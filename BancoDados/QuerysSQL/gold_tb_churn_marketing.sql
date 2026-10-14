create table projeto_churn.gold.tb_churn_marketing(
	id int not null,
	genero varchar(1) not null,
	idade int not null,
	uf varchar(2) not null,
	ind_cliente int not null,
	ano_mes int not null,
	estado_civil varchar(50) not null,
	escolaridade varchar(50) not null,
	mensalidade int not null,
	participacao int not null
);

alter table projeto_churn.gold.tb_churn_marketing
add data_insercao varchar(30) not null;