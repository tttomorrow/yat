-- @testpoint: delete 删除表中某个字段

drop table if exists alter_table_tb07;
create table alter_table_tb07
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb07 values('11',null,'sss');
insert into alter_table_tb07 values('21','','sss');
insert into alter_table_tb07 values('31',66,'');
insert into alter_table_tb07 values('41',66,null);
insert into alter_table_tb07 values('41',66,null);
select * from alter_table_tb07;
delete from alter_table_tb07 where c1=41;
select * from alter_table_tb07;
drop table if exists alter_table_tb07;