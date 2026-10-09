create table projeto_churn.silver.tb_churn_marketing(
	id int not null,
	genero varchar(1) not null,
	codestadocivil int not null,
	idade int not null,
	uf varchar(2) null,
	codescolatidade int null,
	indcliente int null,
	ano_mes int null,
	data_insercao varchar(30) not null
);
