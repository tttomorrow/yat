-- @testpoint: truncate table 与 CASCADE结合
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
select *  from alter_table_tb03;
truncate table alter_table_tb03 CASCADE;
select *  from alter_table_tb03;
drop table if exists alter_table_tb03;
