-- @testpoint: default '正常值' 对检查约束的影响，违反检查约束合理报错
drop table if exists alter_table_tb012;
CREATE TABLE alter_table_tb012 ( a VARCHAR(255) null, b CLOB NULL, c varchar(10) default 'abc');
insert into alter_table_tb012 values('','3','4');
insert into alter_table_tb012 values('3','3',null);
ALTER TABLE alter_table_tb012 ADD  CONSTRAINT con_tb_001 check(c != '');
insert into alter_table_tb012 values('3','3','');
drop table if exists alter_table_tb012;
CREATE TABLE alter_table_tb012 ( a VARCHAR(255) null, b CLOB NULL, c varchar(10) default 'abc');
insert into alter_table_tb012 values('','3','4');
insert into alter_table_tb012 values('3','3','');
ALTER TABLE alter_table_tb012 ADD  CONSTRAINT con_tb_001 check(c ='');
insert into alter_table_tb012 values('3','3',null);
drop table if exists alter_table_tb012;