-- @testpoint: 关闭表的行访问控制开关(ENABLE ROW LEVEL SECURITY)

drop table if exists alter_table_tb036;
create table alter_table_tb036
(
c1 int,
c2 bigint,
c3 varchar(20)
);
ALTER TABLE alter_table_tb036 DISABLE ROW LEVEL SECURITY;
insert into alter_table_tb036 values('11',null,'sss');
insert into alter_table_tb036 values('21','','sss');
insert into alter_table_tb036 values('31',66,'');
insert into alter_table_tb036 values('41',66,null);
insert into alter_table_tb036 values('41',66,null);

ALTER TABLE alter_table_tb036 ENABLE ROW LEVEL SECURITY;
drop table if exists alter_table_tb036;