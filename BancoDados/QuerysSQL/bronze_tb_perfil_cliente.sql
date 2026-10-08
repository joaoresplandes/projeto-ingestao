create table projeto_churn.bronze.tb_perfil_cliente(
	id int not null,
	ind_coparticipacao varchar(1) not null,
	vlr_mensal decimal(10, 2) null,
	vlr_coparticipacao decimal(10, 2) null,
	constraint perfil_cliente_pk primary key (id)
);