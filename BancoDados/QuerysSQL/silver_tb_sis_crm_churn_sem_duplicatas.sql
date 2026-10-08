create table projeto_churn.silver.tb_sis_crm_churn_sem_duplicatas(
	id int not null,
	cpf bigint not null,
	nome varchar(100) not null,
	sobrenome varchar(100) not null,
	idgenero varchar(1) null,
	estado_civil smallint null,
	idade smallint null,
	uf varchar(2) null,
	escolaridade smallint null,
	indcliente smallint null,
	mes varchar(2) null,
	ano varchar(4) null,
	dt_atualizacao varchar(30) not null
);
