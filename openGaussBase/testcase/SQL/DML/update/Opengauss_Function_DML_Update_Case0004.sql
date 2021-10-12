-- @testpoint: 同时更新表的多个字段，成功
-- @modify at: 2020-11-17
--建表
drop table if exists  all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50) );
--插入数据
insert into all_datatype_tbl values(1,'aaaaa'),(2,'bbbbb'),(3,'ccccccccc'),(4,'ddddddddddddd'),(5,'eeeeeeeeeee');
--更新两个字段值
update all_datatype_tbl set (c_varchar,c_integer) = ('abc',1);
--删表
drop table all_datatype_tbl;

