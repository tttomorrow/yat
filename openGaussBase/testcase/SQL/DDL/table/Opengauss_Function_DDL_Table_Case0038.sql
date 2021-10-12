-- @testpoint: 开启表的行访问控制开关(DISABLE ROW LEVEL SECURITY)

drop table if exists alter_table_tb038;
create table alter_table_tb038
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb038 values('11',null,'sss');
insert into alter_table_tb038 values('21','','sss');
insert into alter_table_tb038 values('31',66,'');
insert into alter_table_tb038 values('41',66,null);
insert into alter_table_tb038 values('41',66,null);
ALTER TABLE alter_table_tb038 DISABLE ROW LEVEL SECURITY;
drop table if exists alter_table_tb038;

