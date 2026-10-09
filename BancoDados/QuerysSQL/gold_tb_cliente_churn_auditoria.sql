create table gold.tb_cliente_churn_auditoria(
		id int not null,
		cpf varchar(11) not null,
		nome_completo varchar(100) not null,
		genero varchar(1) not null,
		ind_cliente int not null,
		ano_mes int not null,
		data_insercao varchar(30) not null
);