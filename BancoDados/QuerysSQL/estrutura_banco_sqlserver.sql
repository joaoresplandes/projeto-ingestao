IF DB_ID(N'projeto_churn') IS NULL
    CREATE DATABASE projeto_churn;
GO

USE projeto_churn;
GO

-- 2) Schemas (cada CREATE SCHEMA precisa ser a primeira instrução do batch)
IF SCHEMA_ID(N'bronze') IS NULL EXEC(N'CREATE SCHEMA bronze AUTHORIZATION dbo');
IF SCHEMA_ID(N'silver') IS NULL EXEC(N'CREATE SCHEMA silver AUTHORIZATION dbo');
IF SCHEMA_ID(N'gold') IS NULL EXEC(N'CREATE SCHEMA gold AUTHORIZATION dbo');
GO


-- 3) Tabelas do schema dos bancos
CREATE TABLE bronze.tb_escolaridade(
	id_escolaridade int not null,
	desc_escolaridade varchar(100) null,
	dt_atualizacao varchar(30) not null
);

create table bronze.tb_estado_civil(
	id_ec int not null,
	dsc_ec varchar(100) null,
	dt_atualizacao varchar(30) not null
);

create table bronze.tb_sis_crm_churn(
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

create table bronze.tb_perfil_cliente(
	id int not null,
	ind_coparticipacao varchar(1) not null,
	vlr_mensal decimal(10, 2) null,
	vlr_coparticipacao decimal(10, 2) null,
	constraint perfil_cliente_pk primary key (id)
);

create table silver.tb_cliente_churn_auditoria(
		id int not null,
		cpf varchar(11) not null,
		nome_completo varchar(100) not null,
		ind_cliente int not null,
		ano_mes int not null,
		data_insercao timestamp not null,
		genero varchar(1) not null
);

create table silver.tb_sis_crm_churn(
	id int not null,
	cpf int not null,
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