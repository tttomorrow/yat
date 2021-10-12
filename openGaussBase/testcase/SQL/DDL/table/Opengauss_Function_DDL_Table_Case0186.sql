-- @testpoint: DROP 删除指定的表
drop table if exists alter_table_tb01;
create table alter_table_tb01
(
c1 int,
c2 bigint,
c3 varchar(20)
);

insert into alter_table_tb01 values('11',null,'sss');
insert into alter_table_tb01 values('21','','sss');
insert into alter_table_tb01 values('31',66,'');
insert into alter_table_tb01 values('41',66,null);
insert into alter_table_tb01 values('41',66,null);
create table alter_table_tb02
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb02 values('11',null,'sss');
insert into alter_table_tb02 values('21','','sss');
insert into alter_table_tb02 values('31',66,'');
insert into alter_table_tb02 values('41',66,null);
insert into alter_table_tb02 values('41',66,null);
drop table if exists alter_table_tb01;
drop table if exists alter_table_tb02;