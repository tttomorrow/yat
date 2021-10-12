-- @testpoint: alter table 为新增列添加check约束，在违背条件时合理报错

drop table if exists alter_table_tb012;
CREATE TABLE alter_table_tb012 ( a VARCHAR(255) null, b CLOB NULL, c varchar(10) default 'abc');
insert into alter_table_tb012 values('3','3','4');
insert into alter_table_tb012 values('3','3','');
insert into alter_table_tb012 values('3','3',null);
ALTER TABLE alter_table_tb012 ADD d varchar(10) default '';
ALTER TABLE alter_table_tb012 ADD  CONSTRAINT con_tb_002 check(d ='');
insert into alter_table_tb012 values('3','3','','');
insert into alter_table_tb012 values('3','3',null,null);
insert into alter_table_tb012 values('3','3',null,'ss');
ALTER TABLE alter_table_tb012  ALTER  c  set default '';
ALTER TABLE alter_table_tb012  ALTER  d  set default null;
drop table alter_table_tb012;



