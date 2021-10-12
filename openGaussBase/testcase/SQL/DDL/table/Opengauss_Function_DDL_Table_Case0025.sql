-- @testpoint: alter table 添加check约束，在有违背数据时合理报错
drop table if exists alter_table_tb003;
create table alter_table_tb003(c1 int,c2 bigint,c3 varchar(20));
insert into alter_table_tb003 values('11',null,'sss');
insert into alter_table_tb003 values('21','','sss');
insert into alter_table_tb003 values('31',66,'');
insert into alter_table_tb003 values('41',66,null);
alter table alter_table_tb003 add constraint con_al_table_3_3  check(c3!= '');
alter table alter_table_tb003 add constraint con_al_table_3_1  check(c1!= '');
insert into alter_table_tb003 values('',66,'');
alter table alter_table_tb003 add constraint con_al_table_3_31  check(c3!= 'sss');
alter table alter_table_tb003 add constraint con_al_table_3_11  check(c1!= '21');
insert into alter_table_tb003 values('',66,'sss');
insert into alter_table_tb003 values('21',66,'');
drop table if exists alter_table_tb003;