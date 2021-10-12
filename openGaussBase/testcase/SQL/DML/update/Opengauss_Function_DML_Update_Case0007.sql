-- @testpoint: 根据子查询的结果，作为更新列的新值，子查询结果集有多行，合理报错
-- @modify at: 2020-11-17
--建表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50));
--插入数据
insert into all_datatype_tbl values(1,'aaaaa'),(2,'bbbbb'),(3,'ccccccccc'),(4,'ddddddddddddd'),(5,'eeeeeeeeeee');
--更新数据，报错
update all_datatype_tbl set (c_integer,c_varchar) = (select c_integer,c_varchar from all_datatype_tbl);
--删表
drop table all_datatype_tbl;



