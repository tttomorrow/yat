-- @testpoint: delete 删除表中数据
drop table if exists alter_table_tb06;
create table alter_table_tb06
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb06 values('11',null,'sss');
insert into alter_table_tb06 values('21','','sss');
insert into alter_table_tb06 values('31',66,'');
insert into alter_table_tb06 values('41',66,null);
insert into alter_table_tb06 values('41',66,null);
select * from alter_table_tb06;
delete from alter_table_tb06;
select * from alter_table_tb06;
drop table if exists alter_table_tb06;