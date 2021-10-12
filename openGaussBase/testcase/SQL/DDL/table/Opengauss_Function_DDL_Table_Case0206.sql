-- @testpoint: alter table对有空值的列设置not nul约束时合理报错

drop table if exists alter_table_tb001;
create table alter_table_tb001
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb001 values('11',null,'sss');
insert into alter_table_tb001 values('21','','sss');
insert into alter_table_tb001 values('31',66,'');
insert into alter_table_tb001 values('41',66,null);

alter table alter_table_tb001 modify c3 varchar(50);
alter table alter_table_tb001 modify c3  not null;  --error

drop table if exists alter_table_tb001;