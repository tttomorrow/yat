-- @testpoint: truncate table
drop table if exists alter_table_tb08;
create table alter_table_tb08
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb08 values('11',null,'sss');
insert into alter_table_tb08 values('21','','sss');
insert into alter_table_tb08 values('31',66,'');
insert into alter_table_tb08 values('41',66,null);
insert into alter_table_tb08 values('41',66,null);
select * from alter_table_tb08;
truncate table alter_table_tb08;
select * from alter_table_tb08;
drop table if exists alter_table_tb08;
