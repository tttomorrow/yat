-- @testpoint: alter table 修改列的唯一属性，在有重复值时合理报错
drop table if exists alter_table_tb002;
create table alter_table_tb002
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb002 values('11',null,'sss');
insert into alter_table_tb002 values('21','','sss');
insert into alter_table_tb002 values('31',66,'');
insert into alter_table_tb002 values('41',66,null);
ALTER TABLE alter_table_tb002 add constraint con_al_table_3_3 unique(c3);
ALTER TABLE alter_table_tb002 add constraint con_al_table_3_1 unique(c1);

--insert into alter_table_tb002 values('41',66,null);
alter table alter_table_tb002 modify c1 not null;
drop table if exists alter_table_tb002;
