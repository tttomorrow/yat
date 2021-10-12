-- @testpoint: update语句中，使用子查询与union结合，合理报错
-- @modify at: 2020-11-17
--建表1
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50));
--插入数据
insert into all_datatype_tbl values(1,'aaaaa');
insert into all_datatype_tbl values(2,'bbbbb');
--查询
select * from all_datatype_tbl;
--建表2
drop table if exists all_datatype_tb2;
create table all_datatype_tb2( c_integer integer, c_varchar varchar(50));
--插入数据
insert into all_datatype_tb2 values(1,'aaaaa');
insert into all_datatype_tb2 values(2,'bbbbb');
insert into all_datatype_tb2 values(2,'aaaaa');
--查询
select * from all_datatype_tb2;
--表1和表2使用union查询
select c_integer c1,c_varchar c2 from all_datatype_tbl union select c_integer c1,c_varchar c2 from all_datatype_tb2 t2 where c_integer=t2.c_integer;
--update中使用union子句，报错
update all_datatype_tbl t1 set (c_integer,c_varchar) = (select c_integer c1,c_varchar c2 from all_datatype_tbl union select c_integer c1,c_varchar c2 from all_datatype_tbl where t1.c_integer=c_integer);
--删表
drop table all_datatype_tbl;
drop table all_datatype_tb2;
