-- @testpoint: truncate table与if exists 结合,合理报错
drop table if exists alter_table_tb03;
create table alter_table_tb03
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb03 values('11',null,'sss');
insert into alter_table_tb03 values('21','','sss');
insert into alter_table_tb03 values('31',66,'');
insert into alter_table_tb03 values('41',66,null);
insert into alter_table_tb03 values('41',66,null);
truncate table if exists alter_table_tb03;
drop table if exists alter_table_tb03;