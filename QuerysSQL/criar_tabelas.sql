create table projeto_churn.bronze.tb_perfil_cliente(
	id int not null,
	ind_coparticipacao varchar(1) not null,
	vlr_mensal decimal(10, 2) null,
	vlr_coparticipacao decimal(10, 2) null,
	constraint perfil_cliente_pk primary key (id)
);

create table projeto_churn.silver.tb_cliente_churn_auditoria(
		id int not null,
		cpf varchar(11) not null,
		nome_completo varchar(100) not null,
		ind_cliente int not null,
		ano_mes int not null,
		data_insercao timestamp not null,
		genero varchar(1) not null
)