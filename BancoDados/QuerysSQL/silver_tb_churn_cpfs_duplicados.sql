create table projeto_churn.silver.tb_churn_cpfs_duplicados(
	id int not null,
	mes varchar(2) not null,
	ano varchar(4) not null,
	cpf bigint not null,
	nome varchar(30) not null,
	sobrenome varchar(30) not null
)
