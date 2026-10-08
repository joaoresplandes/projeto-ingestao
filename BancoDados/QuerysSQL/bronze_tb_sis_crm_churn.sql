create table projeto_churn.bronze.tb_sis_crm_churn(
	id varchar(5) not null,
	cpf varchar(20) not null,
	nome varchar(100) not null,
	sobrenome varchar(100) not null,
	idgenero varchar(20) null,
	estado_civil varchar(5) null,
	idade varchar(5) null,
	uf varchar(2) null,
	escolaridade varchar(5) null,
	indcliente varchar(2) null,
	mes varchar(2) null,
	ano varchar(4) null,
	dt_atualizacao varchar(30) not null
);
